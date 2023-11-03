import os
import copy
import warnings
import git
import glob
import shutil
import pandas as pd
import numpy as np
from pathlib import Path
from os.path import join
from subprocess import check_output
from sklearn.model_selection import ParameterGrid, ParameterSampler
from .amhelpers import load_yaml, save_yaml
from pandas.api.types import is_numeric_dtype

def _extract_jobid(output):
    output = output.decode('utf-8')
    jobid = int(output.split('job')[1])
    return jobid

def _count_configs(dir):
    configs = [f for f in os.listdir(dir) if f.startswith('config')]
    return len(configs)

def _generate_configs(default_config, setting, iterable, config_dir):
    results_dir = default_config['results']['path']
    n_existing_configs = _count_configs(config_dir)
    
    configs = []
    
    for i, x in enumerate(iterable, start=1):
        new_config = copy.deepcopy(default_config)
        new_config['results']['path'] = join(results_dir, '%s_%.3d' % (setting, i))
        
        for parameter, value in x.items():
            parameter = parameter.split('::')
            c = new_config
            j = 0
            k = parameter[j]
            while j < len(parameter) - 1:
                c = c[k]
                j += 1
                k = parameter[j]
            c[k] = value
        
        configs.append(new_config)
        
        save_yaml(new_config, config_dir, 'config%.3d' % (n_existing_configs + i))
    
    return configs

def _create_job_configs(
    default_config,
    search_config,
    setting,
    config_dir,
    random_search=None,
    random_state=None,
    dirname=None
):
    if search_config is None or search_config[setting] is None:
        config = copy.deepcopy(default_config)
        config['results']['path'] = join(config['results']['path'], '%s_001' % setting)
        n_existing_configs = _count_configs(config_dir)
        save_yaml(config, config_dir, 'config%.3d' % (n_existing_configs + 1))
        return [config]
    
    grid_or_distribs = search_config[setting]

    if random_search is None:
        try:
            param_grid = ParameterGrid(grid_or_distribs)
            grid_size = len(param_grid)
            random_search = grid_size > search_config['n_iter']
        except TypeError:
            random_search = True
    
    if random_search:
        n_iter = search_config['n_iter']
        if random_state is None:
            random_state = search_config['seed']
        iterable = ParameterSampler(
            grid_or_distribs,
            n_iter,
            random_state=random_state
        )
    else:
        iterable = ParameterGrid(grid_or_distribs)
    
    if dirname is None:
        dirname = setting
    
    return _generate_configs(default_config, dirname, iterable, config_dir)

def _create_jobscript_from_template(
    template,
    experiment,
    experiment_path,
    setting,
    jobname,
    jobdir=None,
    options={}
):
    with open(template, 'r') as f:
        text = f.read()
    text = text.replace('<EXPERIMENT>', experiment)
    text = text.replace('<EXPERIMENT_PATH>', experiment_path)
    text = text.replace('<SETTING>', setting)
    for key, value in options.items():
        text = text.replace('<%s>' % key.upper(), value)
    if jobdir is None:
        jobdir = experiment_path
    jobscript_path = os.path.join(jobdir, jobname)
    with open(jobscript_path, 'w') as f:
        f.write(text)
    return jobscript_path

class Experiment:
    def __init__(
        self,
        config,
        search_config,
        settings,
        train_job_template,
        pre_job_template,
        post_job_template,
        sweep=False,
        options={'gpu': 'A40'}
    ):
        if sweep and search_config is None:
            raise ValueError("'search_config' must not be None when performing a sweep.")

        self.experiment = config['experiment']
        self.path = config['results']['path']
        self.config = config
        self.search_config = search_config
        self.settings = settings
        self.train_template = train_job_template
        self.pre_template = pre_job_template
        self.post_template = post_job_template
        self.sweep = sweep
        self.options = options

        try:
            repo = git.Repo(search_parent_directories=True)
            with open(join(self.path, 'repo.tar'), 'wb') as fp:
                repo.archive(fp)
            git_info = {
                'branch': repo.active_branch,
                'hash': repo.head.object.hexsha
            }
            with open(join(self.path, 'gitinfo.txt'), 'w') as f:
                print(git_info, file=f)
        except Exception as e:
            warnings.warn('Getting Git info failed: %s.' % str(e))

    def prepare(self):
        save_yaml(self.config, self.path, 'default_config')

        if self.search_config is not None:
            save_yaml(self.search_config, self.path, 'search_config')

        logidr = os.path.join(self.path, 'logs')
        Path(logidr).mkdir()

        jobdir = os.path.join(self.path, 'jobscripts')
        Path(jobdir).mkdir()

        self.create_configs()
        for config in self.configs:
            subdir = config['results']['path']
            Path(subdir).mkdir(parents=True, exist_ok=False)
            save_yaml(config, subdir, 'config')

        self.jobsripcts = {'pre': None, 'main': {}, 'post': None}
        
        # Preprocessing job
        jobscript_path = _create_jobscript_from_template(
            template=self.pre_template,
            experiment=self.experiment,
            experiment_path=self.path,
            setting='none',
            jobname='job_pre',
            jobdir=jobdir,
            options=self.options
        )
        self.jobsripcts['pre'] = jobscript_path

        # Main job(s)
        for setting in self.settings:
            jobname = 'job_%s' % setting
            jobscript_path = _create_jobscript_from_template(
                template=self.train_template,
                experiment=self.experiment,
                experiment_path=self.path,
                setting=setting,
                jobname=jobname,
                jobdir=jobdir,
                options=self.options
            )
            self.jobsripcts['main'][setting] = jobscript_path

        # Postprocessing job
        jobscript_path = _create_jobscript_from_template(
            template=self.post_template,
            experiment=self.experiment,
            experiment_path=self.path,
            setting='none',
            jobname='job_post',
            jobdir=jobdir,
            options=self.options
        )
        self.jobsripcts['post'] = jobscript_path
    
    def _create_sweep_configs(self):
        sweep_config_dir = join(self.path, 'sweep_configs')
        Path(sweep_config_dir).mkdir()

        default_config = copy.deepcopy(self.config)
        results_dir = default_config['results']['path']

        sweep_config = self.search_config['sweep']

        if (
            isinstance(sweep_config, dict)
            and set(self.settings).issubset(sweep_config)
        ):
            sweep_configs = {}
            for setting in self.settings:
                default_config['results']['path'] = join(results_dir, 'sweep_%s' % setting)
                sweep_configs[setting] = _create_job_configs(
                    default_config,
                    sweep_config,
                    setting=setting,
                    config_dir=sweep_config_dir,
                    random_search=False,
                    dirname='sweep'
                )
        else:
            default_config['results']['path'] = join(results_dir, 'sweep')
            sweep_configs = _create_job_configs(
                default_config,
                self.search_config,
                setting='sweep',
                config_dir=sweep_config_dir,
                random_search=False
            )
        
        return sweep_configs

    def create_configs(self):
        self.configs = []
        self.n_jobs_per_setting = {s: 0 for s in self.settings}

        if self.sweep:
            sweep_configs = self._create_sweep_configs()

            for setting in self.settings:
                config_dir = join(self.path, '%s_configs' % setting)
                Path(config_dir).mkdir()
                
                if isinstance(sweep_configs, dict):
                    sweep_configs_setting = sweep_configs[setting]
                else:
                    sweep_configs_setting = sweep_configs
                
                # If a seed is set, we want to control how the configs are generated. This should not
                # depend on the order of the settings, so we create the seeds here and not before the loop.
                np.random.seed(self.search_config['seed'])
                sweep_seeds = np.random.randint(0, 2 ** 16, len(sweep_configs_setting))
                
                for i, sweep_config in enumerate(sweep_configs_setting):
                    configs = _create_job_configs(
                        sweep_config,
                        self.search_config,
                        setting,
                        config_dir,
                        random_state=sweep_seeds[i],
                    )
                    self.configs.extend(configs)
                    self.n_jobs_per_setting[setting] += len(configs)
        else:
            for setting in self.settings:
                config_dir = join(self.path, '%s_configs' % setting)
                Path(config_dir).mkdir()
                configs = _create_job_configs(self.config, self.search_config, setting, config_dir)
                self.configs.extend(configs)
                self.n_jobs_per_setting[setting] = len(configs)
    
    def run(self):
        main_dependencies = [
            self.submit_job(self.jobsripcts['pre'])
        ]
        
        post_dependencies = []
        for setting in self.settings:
            jobid = self.submit_job(
                self.jobsripcts['main'][setting],
                main_dependencies,
                self.n_jobs_per_setting[setting]
            )
            post_dependencies.append(jobid)
        
        self.submit_job(
            self.jobsripcts['post'],
            post_dependencies
        )

    def submit_job(self, jobscript_path, dependencies=None, n_jobs=1):
        command = ['sbatch']
        if dependencies is not None:
            dependencies = [str(d) for d in dependencies]
            command.append('--dependency=afterok:%s' % ':'.join(dependencies))
        if n_jobs > 1:
            command.append('--array=1-%d' % n_jobs)
        command.append(jobscript_path)
        return _extract_jobid(check_output(command))

class Postprocessing:
    def __init__(self, exp_path):
        self.exp_path = exp_path
        self.settings = [
            x.split('_configs')[0]
            for x in os.listdir(exp_path)
            if os.path.isdir(join(exp_path, x))
            and x.endswith('_configs')
            and not x.startswith('sweep')
        ]

    def _sort_scores(self, path, sorter):
        all_sorted_scores = {}
        
        for setting in self.settings:
            experiments = [
                x for x in os.listdir(path)
                if x.startswith(setting)
                and not 'configs'in x
            ]

            csvs, sort_scores = [], []
            
            for e in experiments:
                p = join(path, e, 'scores.csv')
                if not os.path.isfile(p):
                    print('File {} not found.'.format(p))
                    continue
                csv = pd.read_csv(p)
                if not 'subset' in csv.columns:
                    raise ValueError(
                        "Column 'subset' not found in {}.".format(p)
                    )
                csv.insert(0, 'exp', e)
                csvs.append(csv)
                sort_score = sorter(csv)
                assert isinstance(sort_score, float)
                sort_scores.append(sort_score)
            
            if len(csvs) > 0:
                sort_scores = np.array(sort_scores)
                if np.isnan(sort_scores).any():
                    sort_scores[np.isnan(sort_scores)] = -np.inf
                csvs = [csvs[i] for i in np.argsort(sort_scores)[::-1]]
                sorted_scores = pd.concat(csvs, ignore_index=True)
                all_sorted_scores[setting] = sorted_scores
        
        return all_sorted_scores

    def _check_parameters(self, params):
        out = {}
        for param, value in params.items():
            if isinstance(value, list):
                out[param] = '[' + ','.join(map(str, value)) + ']'
            else:
                out[param] = value
        return out

    def _collect_best_scores(
        self,
        sorted_scores,
        sweep_grid,
        setting=None
    ):
        best_scores_list = []
        
        iterable = ParameterGrid(sweep_grid)
        for i_sweep, parameters in enumerate(iterable, start=1):
            sweep_index = '%s_%d' % (setting, i_sweep) if setting else i_sweep
            parameters = self._check_parameters(parameters)
            df = pd.DataFrame({'sweep': sweep_index} | parameters, index=[0])
            
            for scores in sorted_scores[i_sweep-1].values():
                best_exp = scores.exp.iloc[0]
                best_scores = scores.groupby('exp').get_group(best_exp)
                best_scores = pd.concat(
                    (
                        pd.concat(len(best_scores) * [df], ignore_index=True),
                        best_scores,
                    ),
                    axis=1,
                )
                best_scores_list.append(best_scores)
        
        return best_scores_list

    def _concat_scores(self, sorted_scores, sweep_grid=None):
        scores_list = []
        
        if sweep_grid is not None:
            if (
                isinstance(sweep_grid, dict) and
                set(self.settings).issubset(sweep_grid)
            ):
                for setting in self.settings:
                    sorted_scores_setting = [
                        d for d in sorted_scores
                        if setting in d  # setting is the only key in d
                    ]
                    best_scores = self._collect_best_scores(
                        sorted_scores_setting,
                        sweep_grid[setting],
                        setting
                    )
                    scores_list += best_scores
            else:
                scores_list += self._collect_best_scores(sorted_scores, sweep_grid)
        else:
            for scores in sorted_scores.values():
                best_exp = scores.exp.iloc[0]
                best_scores = scores.groupby('exp').get_group(best_exp)
                scores_list.append(best_scores)
        
        scores = pd.concat(scores_list, ignore_index=True)
        return scores[~(scores.subset == 'valid')]

    def _get_sweep_dirs(self):
        outer_sweep_dirs = [
            x for x in os.listdir(self.exp_path) 
            if x.startswith('sweep')
            and not 'configs'in x
        ]
        inner_sweep_dirs = [
            join(d, x)
            for d in outer_sweep_dirs
            for x in os.listdir(join(self.exp_path, d))
            if x.startswith('sweep')
        ]
        return sorted(inner_sweep_dirs)

    def collect_results(self, score_sorter):
        if any([x.startswith('sweep') for x in os.listdir(self.exp_path)]):
            sorted_scores = []
            for d in self._get_sweep_dirs():
                subdir = join(self.exp_path, d)
                sorted_scores += [self._sort_scores(subdir, score_sorter)]
            
            search_config_path = join(self.exp_path, 'search_config.yaml')
            search_config = load_yaml(search_config_path)
            sweep_grid = search_config['sweep']
            
            scores = self._concat_scores(sorted_scores, sweep_grid)
        else:
            sorted_scores = self._sort_scores(self.exp_path, score_sorter)
            scores = self._concat_scores(sorted_scores)
        
        scores.to_csv(join(self.exp_path, 'scores.csv'), index=False)

    def remove_files(self):
        scores_path = join(self.exp_path, 'scores.csv')

        if not os.path.isfile(scores_path):
            raise ValueError(
                'File {} is required but was not found.'.format(
                    scores_path
                )
            )
        
        scores = pd.read_csv(scores_path)

        assert 'sweep' in scores.columns
        assert 'exp' in scores.columns

        if is_numeric_dtype(scores.sweep):
            dirs_to_keep = [
                os.path.join(
                    self.exp_path,
                    'sweep',
                    'sweep_%.3d' % sweep,
                    exp
                )
                for sweep, exp in zip(
                    scores.sweep,
                    scores.exp
                )
            ]
        else:
            dirs_to_keep = [
                os.path.join(
                    self.exp_path,
                    'sweep_%s' % '_'.join(sweep[:-1]),
                    'sweep_%s' % sweep[-1].zfill(3),
                    exp
                )
                for sweep, exp in zip(
                    scores.sweep.str.split('_'),
                    scores.exp
                )
            ]
        dirs_to_keep = set(dirs_to_keep)

        sweep_dirs = self._get_sweep_dirs()
        sweep_dirs = [join(self.exp_path, d) for d in sweep_dirs]
        all_dirs = [
            join(d, x)
            for d in sweep_dirs
            for x in sorted(os.listdir(d))
        ]

        dirs_to_delete = set(all_dirs) - dirs_to_keep

        for d in dirs_to_delete:
            checkpoints = join(d, 'checkpoints')
            if os.path.isdir(checkpoints):
                shutil.rmtree(checkpoints)
            for f in glob.glob(join(d, '*.pt')):
                os.remove(f)
