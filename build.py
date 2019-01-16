import os, sys, shutil, pathlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Build:

    #
    #
    #
    def build_production_database(self):

        with open('database/database.py', 'r') as fin:
        
            data: list = fin.read().splitlines(True)
        
            with open('database/production.py', 'w') as fout:

                fout.writelines(data[8:])


        filenames: [str] = ['database/production_header.py', 'database/production.py']
        
        with open('database/production_database.py', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

    ###################
    ## Normalization ##
    ###################
    def build_normalization_cloud_function(self):

        pathlib.Path('normalization_cloud_function').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('normalization_cloud_function/normalization').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('normalization_cloud_function/models').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('normalization_cloud_function/database').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('normalization_cloud_function/helper').mkdir(parents=True, exist_ok=True) 

        shutil.copy('normalization/normalization.py', 'normalization_cloud_function/normalization/normalization.py')

        shutil.copy('database/production_database.py', 'normalization_cloud_function/database/database.py')

        shutil.copy('models/user.py', 'normalization_cloud_function/models/user.py')
        shutil.copy('models/level.py', 'normalization_cloud_function/models/level.py')
        shutil.copy('models/session.py', 'normalization_cloud_function/models/session.py')
        shutil.copy('models/performance.py', 'normalization_cloud_function/models/performance.py')

        shutil.copy('helper/helper.py', 'normalization_cloud_function/helper/helper.py')

        shutil.copy('normalization/main.py', 'normalization_cloud_function/main.py')
        shutil.copy('requirements.txt', 'normalization_cloud_function/requirements.txt')

    def deploy_normalization_cloud_function(self): 

        self.build_production_database()
        self.build_normalization_cloud_function()

        os.system('gcloud beta functions deploy normalization_cloud_function --runtime python37 --trigger-http --source="normalization_cloud_function"')
        os.remove('database/production.py')
        os.remove('database/production_database.py')

        shutil.rmtree('normalization_cloud_function')


    #############
    ## Cluster ##
    #############
    def build_cluster_cloud_function(self):

        pathlib.Path('cluster_cloud_function').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('cluster_cloud_function/cluster').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('cluster_cloud_function/models').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('cluster_cloud_function/database').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('cluster_cloud_function/helper').mkdir(parents=True, exist_ok=True) 

        shutil.copy('cluster/cluster.py', 'cluster_cloud_function/cluster/cluster.py')
        
        shutil.copy('database/production_database.py', 'cluster_cloud_function/database/database.py')

        shutil.copy('models/user.py', 'cluster_cloud_function/models/user.py')
        shutil.copy('models/level.py', 'cluster_cloud_function/models/level.py')
        shutil.copy('models/session.py', 'cluster_cloud_function/models/session.py')
        shutil.copy('models/performance.py', 'cluster_cloud_function/models/performance.py')
        
        shutil.copy('helper/helper.py', 'cluster_cloud_function/helper/helper.py')

        shutil.copy('cluster/main.py', 'cluster_cloud_function/main.py')
        shutil.copy('requirements.txt', 'cluster_cloud_function/requirements.txt')

    def deploy_cluster_cloud_function(self): 

        self.build_production_database()
        self.build_cluster_cloud_function()

        os.system('gcloud beta functions deploy cluster_cloud_function --runtime python37 --trigger-http --source="cluster_cloud_function"')
        os.remove('database/production.py')
        os.remove('database/production_database.py')

        shutil.rmtree('cluster_cloud_function')

    ###############
    ## Evolution ##
    ###############
    def build_evolution_cloud_function(self):

        pathlib.Path('evolution_cloud_function').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('evolution_cloud_function/evolution').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('evolution_cloud_function/models').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('evolution_cloud_function/database').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('evolution_cloud_function/helper').mkdir(parents=True, exist_ok=True) 

        shutil.copy('evolution/evolution.py', 'evolution_cloud_function/evolution/evolution.py')
        
        shutil.copy('database/production_database.py', 'evolution_cloud_function/database/database.py')

        shutil.copy('models/user.py', 'evolution_cloud_function/models/user.py')
        shutil.copy('models/level.py', 'evolution_cloud_function/models/level.py')
        shutil.copy('models/session.py', 'evolution_cloud_function/models/session.py')
        shutil.copy('models/performance.py', 'evolution_cloud_function/models/performance.py')
        
        shutil.copy('helper/helper.py', 'evolution_cloud_function/helper/helper.py')
        
        shutil.copy('evolution/main.py', 'evolution_cloud_function/main.py')
        shutil.copy('requirements.txt', 'evolution_cloud_function/requirements.txt')

    def deploy_evolution_cloud_function(self): 

        self.build_production_database()
        self.build_evolution_cloud_function()

        os.system('gcloud beta functions deploy evolution_cloud_function --runtime python37 --trigger-http --source="evolution_cloud_function"')
        os.remove('database/production.py')
        os.remove('database/production_database.py')

        shutil.rmtree('evolution_cloud_function')

if __name__ == "__main__": 

    build: Build = Build()

    # build.deploy_normalization_cloud_function()
    # build.deploy_cluster_cloud_function()
    build.deploy_evolution_cloud_function()

