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


    ###############
    ## Evolution ##
    ###############
    def build_cluster_function(self):

        pathlib.Path('cluster_cloud_function').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('cluster_cloud_function/cluster').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('cluster_cloud_function/models').mkdir(parents=True, exist_ok=True) 
        pathlib.Path('cluster_cloud_function/database').mkdir(parents=True, exist_ok=True) 

        shutil.copy('cluster/cluster.py', 'cluster_cloud_function/cluster/cluster.py')
        
        shutil.copy('database/production_database.py', 'cluster_cloud_function/database/database.py')

        shutil.copy('models/user.py', 'cluster_cloud_function/models/user.py')
        shutil.copy('models/level.py', 'cluster_cloud_function/models/level.py')
        shutil.copy('models/session.py', 'cluster_cloud_function/models/session.py')
        shutil.copy('models/performance.py', 'cluster_cloud_function/models/performance.py')
        
        shutil.copy('cluster/main.py', 'cluster_cloud_function/main.py')
        shutil.copy('requirements.txt', 'cluster_cloud_function/requirements.txt')


if __name__ == "__main__": 

    build: Build = Build()

    build.build_production_database()

    build.build_cluster_function()
    os.system('gcloud beta functions deploy cluster_cloud_function --runtime python37 --trigger-http --source="cluster_cloud_function"')
    os.remove('database/production.py')
    os.remove('database/production_database.py')
    shutil.rmtree('cluster_cloud_function')

