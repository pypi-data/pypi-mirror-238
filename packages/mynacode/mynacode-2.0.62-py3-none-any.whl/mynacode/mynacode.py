import numpy as np
import pandas as pd
import os, sys
import json, requests, ast
from datetime import datetime
from sklearn import metrics
import matplotlib.pyplot as plt
import dill
import pickle
import urllib.request
from pathlib import Path
import glob, re, pkg_resources
import shutil, yaml, random, string
import time, copy


try:
    import torch
    import torch.nn as nn
    import torchvision
    from torch.utils.data import Dataset, DataLoader, ConcatDataset
    import torch.nn.functional as F
except ImportError:
    pass

try:
    import keras
except ImportError:
    try:
      import tensorflow.keras as keras
    except:
      pass

try:
    import tensorflow as tf
except ImportError:
    pass

import warnings
import functools

# Decorator function to suppress warnings within a specific function
def suppress_warnings(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            result = func(*args, **kwargs)
        return result
    return wrapper

protocol = 'https'
IP = 'mynacode.com'

#protocol = 'http'
#IP = '127.0.0.1:8000'


uname = ""
ky = ""
run_id_global = ""
project_id_global = ""
run_dir_global = ""
project_dir_global = ""
prev_max = -9999999999
prev_min = 9999999999
metric_values = []
index_count = 0
sweep_global = False
save_best_results = False
first_sweep_run = False
dataset_dict = {}
results_dict = {}
track_config = {}
auth_failed = True
disable = False
saved_models = []



def login(username, key):
  global uname
  global ky
  global auth_failed

  print("Logging in...")
  credentials = {'username':username, 'key':key, 'task':'login'}
  response = requests.post(protocol+'://'+IP+'/api/python_login', data=credentials)

  if response.text == '1':
    uname = username
    ky = key
    auth_failed = False
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")
    auth_failed = True


def create_project(project_name = "", project_directory = ""):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.create_project()")
      return

    data = {'project_name': project_name, 'project_directory': project_directory, 'username': uname, 'key': ky}
    response = requests.post(protocol+'://'+IP+'/api/create_project_python', data=data)

    return response.text


def create_run(project_id = None, sweep = False, sweep_name = "", run_name = ""):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.create_run()")
      return

    if not project_id:
      print("Please provide project ID")
      return

    data = {'project_id': project_id, 'username': uname, 'key': ky, 'sweep': sweep, 'sweep_name': sweep_name, 'run_name': run_name}
    response = requests.post(protocol+'://'+IP+'/api/create_run_python', data=data)

    return response.text


def disable(value = False):
    global disable
    disable = value


def save_files(run = None):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
        print("Please login using mynacode.login(Username, Key) before calling mynacode.init()")
        return

    if run_dir_global == "":
        print("Please run mynacode.start(...) to create a run before calling this function")
        return

    py_files = glob.glob('./**/*.py', recursive=True)
    ipynb_files = glob.glob('./**/*.ipynb', recursive=True)

    if not os.path.exists(run_dir_global+'/files/'):
        os.mkdir(run_dir_global+'/files/')

    for file in py_files:
        shutil.copy(file, run_dir_global+'/files/')

    for file in ipynb_files:
        shutil.copy(file, run_dir_global+'/files/')

    data = {'run_id' : run_id_global, 'config_dict': str({"python_files_path":run_dir_global+'/files/'}), 'node_name': "Datasets", 'username': uname, 'key': ky}
    
    response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)

def start(base_folder = "", project = "", sweep = False, sweep_name = "", run_name=""):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
        print("Please login using mynacode.login(Username, Key) before calling mynacode.init()")
        return


    global project_id_global
    global project_dir_global
    global prev_max
    global prev_min
    global metric_values
    global metric_index
    global index_count
    global run_dir_global
    global run_id_global
    global first_sweep_run
    global sweep_global


    prev_max = -9999999999
    prev_min = 9999999999
    metric_values = []
    metric_index = 0
    index_count = 0


    if len(base_folder) == 0:
      base_folder = Path.cwd().as_posix()
    elif not os.path.exists(base_folder):
      print("Using current working directory. Path not found: ", base_folder)
      base_folder = Path.cwd().as_posix()

    if not os.path.exists(base_folder+'/'+'mynacode'):
      os.mkdir(base_folder+'/mynacode')

    if len(project) == 0:
      project = 'Project'

    if not os.path.exists(base_folder+'/mynacode/'+project):
      os.mkdir(base_folder+'/mynacode/'+project)

    project_dir_global = base_folder+'/mynacode/'+project
    project_id_global = create_project(project, project_dir_global)
    print("Project Directory: ", project_dir_global)

    prev_max = -9999999999
    prev_min = 9999999999
    metric_values = []
    metric_index = 0
    index_count = 0
    start_time, end_time = 0, 0


    config_dict={}

    if sweep == True:
      sweep_global = True
      first_sweep_run = True

      if len(str(sweep_name)) == 0:
        sweep_name = ""
      else:
        sweep_name = sweep_name

      r_id = create_run(int(project_id_global), sweep = True, sweep_name = sweep_name)
      run_id_global = r_id

      if len(str(sweep_name)) == 0:  
          run_dir_global = project_dir_global+'/S'+str(r_id)
      else:
          run_dir_global = project_dir_global+'/S'+str(r_id)+'-'+sweep_name
          
      os.mkdir(run_dir_global)
      config_dict.update({'sweep': sweep,'sweep_name': sweep_name, 'sweep_path': run_dir_global})
    else:
      sweep_global = False
      first_sweep_run = False
      r_id = create_run(int(project_id_global), run_name = run_name)
      run_id_global = r_id
      
      if len(str(run_name)) == 0:
        run_name = ""
      else:
        run_name = run_name

      if len(str(run_name)) == 0:  
          run_dir_global = project_dir_global+'/R'+str(r_id)
      else:
          run_dir_global = project_dir_global+'/R'+str(r_id)+'-'+run_name
          
      os.mkdir(run_dir_global)
      config_dict.update({'run_name': run_name, 'run_path': run_dir_global})

    print("Run ID: ", str(r_id)) 
    print("Run Directory: ", run_dir_global)

    installed_packages = pkg_resources.working_set #Save all installed packages for that project
    installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])
    config_dict.update({"installed_packages":installed_packages_list})

    data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': uname, 'key': ky}

    response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)




def csv(df, name='dataframe', run_id=None):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
        print("Please login using mynacode.login(Username, Key) before calling mynacode.csv()")
        return

    if run_dir_global == "":
        print("Please run mynacode.init(...) to create a run before calling this function")
        return

    if not run_id:
        run_id = run_id_global

    columns_list = df.columns.values.tolist()
    isnull_list = df.isnull().sum().values.tolist()
    isunique_list = df.nunique().values.tolist()
    size = sys.getsizeof(df)/1024
    shape = df.shape
    dtypes_list = []

    for d in df.dtypes:
        dtypes_list.append(str(d))

    if not os.path.exists(project_dir_global+'/csv'):
        os.mkdir(project_dir_global+'/csv')

    save_new_data_flag = 1
    
    csv_files = os.listdir(project_dir_global+'/csv')
    if len(csv_files) != 0:       
        paths = [os.path.join(project_dir_global+'/csv', basename) for basename in csv_files]
        newest_csv_file =  max(paths, key=os.path.getctime)
        newest_df = pd.read_csv(newest_csv_file)

        if newest_df.equals(df):
            print("The current dataframe csv is already saved locally at "+ newest_csv_file + ".")
            save_new_data_flag = 0    
        
    if save_new_data_flag == 1:
        df.to_csv(project_dir_global+'/csv/'+name+'.csv', index=False)
        print("Dataframe CSV path: " + project_dir_global+'/csv/'+name+'.csv')

        data = {'run_id': run_id, 'columns_list': str(columns_list), 'isnull_list': str(isnull_list),
                'isunique_list': str(isunique_list), 'dtypes_list': str(dtypes_list),
                'username': uname, 'size': int(size), 'shape': str(shape), 'key': ky, 'node_name': 'CSV', 'csv_path': project_dir_global+'/csv/'+name+'.csv'}
        response = requests.post(protocol+'://'+IP+'/api/add_csv', data=data)

        if response.text == '0':
          print("Authentication failed")
        else:
          print("CSV Information saved.")


def evenly_spaced_points(fpr, tpr, N):
    if N <= 0:
        return []

    if N == 1:
        return [fpr[np.argmin(fpr)]]

    step_size = (len(fpr) - 1) / (N - 1)

    indices = [int(round(i * step_size)) for i in range(N)]

    selected_points_fpr = [fpr[i] for i in indices]
    selected_points_tpr = [tpr[i] for i in indices]

    return selected_points_fpr, selected_points_tpr



def specificity(y_true, y_pred):
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_truth = np.count_nonzero(y_true == 0)

    return float(y_correct/y_truth)

def npv(y_true, y_pred): #Negative Predicted Value
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_predicted = np.count_nonzero(y_pred == 0)

    return float(y_correct/y_predicted)

def get_roc_auc(y_true, y_pred):
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_pred)
    roc_auc = metrics.auc(fpr, tpr)
    gmeans = np.sqrt(tpr * (1 - fpr)) #sensitivity * specificity (element-wise)
    index = np.argmax(gmeans) #Returns index of max value
    best_threshold = threshold[index]

    return fpr, tpr, roc_auc, gmeans, best_threshold, index

def get_metrics(y_true, y_pred, threshold):
    y_pred_binary = (y_pred > threshold).astype('float')

    prec = metrics.precision_score(y_true, y_pred_binary)
    rec = metrics.recall_score(y_true, y_pred_binary)
    spec = specificity(y_true, y_pred_binary)
    f1 = metrics.f1_score(y_true, y_pred_binary)
    acc = metrics.accuracy_score(y_true, y_pred_binary)
    npv_val = npv(y_true, y_pred_binary)

    c_matrix = metrics.confusion_matrix(y_true, y_pred_binary, labels=[0,1])

    c_matrix = c_matrix.tolist()

    c_matrix = [item for sublist in c_matrix for item in sublist]

    return prec, rec, spec, f1, acc, npv_val, c_matrix


def save_file(run_id, filepath):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.save_file()")
      return

    if not os.path.exists(filepath):
      print(filepath, ' doesn not exist')
      return

    file = {'file': open(filepath,'rb')}

    response = requests.post(protocol+'://'+IP+'/api/upload_file', files=file, data={'run_id':run_id, 'username': uname, 'key': ky})


def log(config_dict = {}, run_id = None):

  if disable == False:
    print("Mynacode disabled. To enable, set mynacode.disable(False)")
    return

  if auth_failed == True:
    print("Please login using mynacode.login(Username, Key) before calling mynacode.config()")
    return

  if run_dir_global == "":
    print("Please run mynacode.init(...) to create a run before calling this function")
    return

  if not run_id:
    run_id = run_id_global

  if config_dict:
    file=open(run_dir_global+"/config.yaml","w")
    yaml.dump(config_dict,file)
    file.close()
    config_dict.update({'config_file_path': run_dir_global+"/config.yaml"})

  data = {'run_id' : run_id, 'config_dict': str(config_dict), 'node_name': 'Datasets', 'username': uname, 'key': ky}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)


'''
def torch_model(model=None, name='best_model_chkpt', metric_name=None, metric_value=None, goal='maximize', epoch=None, track={}, run_id=None):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.torch_model()")
      return

    if isinstance(metric_value, torch.Tensor):
      metric_value = float(metric_value.cpu().numpy())
    else:
      metric_value = float(metric_value)

    global prev_min
    global prev_max
    global metric_values
    global index_count
    results_dict = {}

    if run_dir_global == "":
      print("Please run mynacode.init(...) to create a run before calling this function")
      return

    if not os.path.exists(run_dir_global+'/model'):
      os.mkdir(run_dir_global+'/model')

    if model:
      with open(run_dir_global+'/saved_network.pkl', 'wb') as f:
          dill.dump(model, f, protocol=4)

      metric_values.append(metric_value)

      if goal == 'maximize':
        if metric_value > prev_max:
          prev_max = metric_value
              
          results_dict.update({'metric_name': metric_name})
          results_dict.update({'metric_goal': 'maximize'})
          results_dict.update({'best_'+metric_name: metric_value})
          results_dict.update({'best_metric_index': index_count})
          results_dict.update({'best_'+metric_name+'_epoch': epoch})

          #torch.save(model.state_dict(), run_dir_global+'/best_model_chkpt.pt')

          for filename in os.listdir(run_dir_global+'/'):
            if filename.endswith('.pt'):
              file_path = os.path.join(run_dir_global+'/', filename)
              os.remove(file_path)
              
          torch.save(model.state_dict(), run_dir_global+'/'+name+'.pt')

          with open(run_dir_global+'/best_model_logs.txt', 'w') as f:
            f.write('Metric: '+ str(results_dict['metric_name']))
            f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
            f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch']))

          model_dict = {'library':'PyTorch', 'metric_values': metric_values,
                              'best_model_statedict_path': run_dir_global+'/'+name+'.pt',
                              'best_model_network_path': run_dir_global+'/saved_network.pkl',
                              'best_model_logs_path': run_dir_global+'/best_model_logs.txt'}

          config_dict = {**model_dict, **results_dict, **track}

          results(results_dict = config_dict, run_id = None)
        else:
          results(results_dict = {'metric_values': metric_values}, run_id = None)

      elif goal == 'minimize':
        if metric_value < prev_min:
          prev_min = metric_value
              
          results_dict.update({'metric_name': metric_name})
          results_dict.update({'metric_goal': 'minimize'})
          results_dict.update({'best_'+metric_name: metric_value})
          results_dict.update({'best_metric_index': index_count})
          results_dict.update({'best_'+metric_name+'_epoch': epoch})

          #torch.save(model.state_dict(), run_dir_global+'/best_model_chkpt.pt')

          for filename in os.listdir(run_dir_global+'/'):
            if filename.endswith('.pt'):
              file_path = os.path.join(run_dir_global+'/', filename)
              os.remove(file_path)
              
          torch.save(model.state_dict(), run_dir_global+'/'+name+'.pt')
          

          with open(run_dir_global+'/best_model_logs.txt', 'w') as f:
            f.write('Metric: '+ str(results_dict['metric_name']))
            f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
            f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch']))

          model_dict = {'library':'PyTorch', 'metric_values': metric_values,
                              'best_model_statedict_path': run_dir_global+'/'+name+'.pt',
                              'best_model_network_path': run_dir_global+'/saved_network.pkl',
                              'best_model_logs_path': run_dir_global+'/best_model_logs.txt'}

          config_dict = {**model_dict, **results_dict, **track}

          results(results_dict = config_dict, run_id = None)
        else:
          results(results_dict = {'metric_values': metric_values}, run_id = None)

      index_count += 1
    else:
      print("Please specify a Pytorch model.")
      return
'''


def torch_model(model=None, name='best_model_chkpt', metric_name=None, metric_value=None, epoch=None, track={}, run_id=None):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.torch_model()")
      return

    if isinstance(metric_value, torch.Tensor):
      metric_value = float(metric_value.cpu().numpy())
    else:
      metric_value = float(metric_value)

    results_dict = {}

    if run_dir_global == "":
      print("Please run mynacode.init(...) to create a run before calling this function")
      return


    if model:
      with open(run_dir_global+'/saved_network.pkl', 'wb') as f:
          dill.dump(model, f, protocol=4)

              
      results_dict.update({'metric_name': metric_name})
      results_dict.update({'best_'+metric_name: metric_value})
      results_dict.update({'best_'+metric_name+'_epoch': epoch})

      for filename in os.listdir(run_dir_global+'/'):
        if ((filename.endswith('.pt')) and (filename not in saved_models)):
          file_path = os.path.join(run_dir_global+'/', filename)
          os.remove(file_path)
          
      torch.save(model.state_dict(), run_dir_global+'/'+name+'.pt')


      with open(run_dir_global+'/model_logs.txt', 'a') as f:
        f.write('\nModel Name: '+ str(name+'.pt'))
        f.write('\nMetric: '+ str(results_dict['metric_name']))
        f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
        f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch'])+'\n')

      model_dict = {'library':'PyTorch',
                          'best_model_statedict_path': run_dir_global+'/'+name+'.pt',
                          'best_model_network_path': run_dir_global+'/saved_network.pkl',
                          'best_model_logs_path': run_dir_global+'/best_model_logs.txt'}

      config_dict = {**model_dict, **results_dict, **track}

      results(results_dict = config_dict, run_id = None)
    else:
      print("Please specify a Pytorch model.")
      return


def run_reset():

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.torch_refresh()")
      return

    global metric_values
    global index_count
    global saved_models
    global prev_min
    global prev_max

    for filename in os.listdir(run_dir_global+'/'):
        if filename.endswith('.pt') or filename.endswith('.hdf5'):
            saved_models.append(filename)

    saved_models = list(set(saved_models))

    with open(run_dir_global+'/model_logs.txt', 'a') as f:
        f.write('\n\n  ------ New Run ------')
    
    index_count = 0
    metric_values = []
    prev_max = -9999999999
    prev_min = 9999999999





def newest(path):
    files = os.listdir(path)
    if len(files) == 0:
        return None
    paths = [os.path.join(path, basename) for basename in files]
    newest_data_folder =  max(paths, key=os.path.getctime)

    try:
        temp = re.split(r'[\\/]', newest_data_folder)[-1].split('-')[-1]
        print("The path to the most recent dataset stored on the local machine:\n"+newest_data_folder)
        return newest_data_folder
    except:
        return None


def np_data(x_train=[], y_train=[], x_val=[], y_val=[], x_test=[], y_test=[], name="dataset", if_sweep_save_once = True, run_id = None):

  if disable == False:
    print("Mynacode disabled. To enable, set mynacode.disable(False)")
    return


  if auth_failed == True:
    print("Please login using mynacode.login(Username, Key) before calling mynacode.data()")
    return

  global first_sweep_run

  if (if_sweep_save_once == True) and (first_sweep_run == False) and (sweep_global == True):
    print("Dataset saved on first run. Subsequent 'data()' calls in the current sweep are ignored. To create a new sweep, run 'init()', or, for repeated calls within a sweep, set 'if_sweep_save_once = False'.")
    return

  config_dict = {}

  x_train = np.array(x_train)
  x_val = np.array(x_val)
  x_test = np.array(x_test)

  y_train = np.array(y_train)
  y_val = np.array(y_val)
  y_test = np.array(y_test)

  if project_dir_global == "":
    print("Please run mynacode.start(...) to initialize a project before calling this function")
    return
  current_dir = project_dir_global

  if run_id_global == "":
    print("Please run mynacode.init(...) to initialize a run before calling this function")
    return


  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  name = name.replace("-", "")

  if sweep_global == True:
      dataset_folder = "S"+str(run_id_global)+"-"+name
  else:
      dataset_folder = "R"+str(run_id_global)+"-"+name

  # Check latest dataset folder
  save_new_data_flag = 0
  newest_data_folder = newest(current_dir+'/data')


  if newest_data_folder == None:
      save_new_data_flag = 1
  elif re.split(r'[\\/]', newest_data_folder)[-1].split('-')[-1] != name:
      save_new_data_flag = 1
  else:
      if (len(y_train) > 0) and (os.path.exists(newest_data_folder + '/y_train.pkl')): #Both exist
          percent_20 = int((20/100)*len(y_train))

          with open(newest_data_folder + '/y_train.pkl', 'rb') as f:
              x = dill.load(f)

              if not np.array_equal(x[:percent_20], y_train[:percent_20]): #Both exist but not equal
                  save_new_data_flag = 1
              else:
                  config_dict.update({'y_train_path': newest_data_folder + '/y_train.pkl'})
                  config_dict.update({'x_train_path': newest_data_folder + '/x_train.pkl'})
                  
      elif (~(os.path.exists(newest_data_folder + '/y_train.pkl'))) and (len(y_train) == 0): #Both don't exist
          pass
      else: #One exists, one doesn't
          save_new_data_flag = 1

      if ((os.path.exists(newest_data_folder + '/y_val.pkl')) and (save_new_data_flag == 0) and (len(y_val) > 0)):
          percent_20 = int((20/100)*len(y_val))

          with open(newest_data_folder + '/y_val.pkl', 'rb') as f:
              x = dill.load(f)

              if not np.array_equal(x[:percent_20], y_val[:percent_20]):
                  save_new_data_flag = 1
              else:
                  config_dict.update({'y_val_path': newest_data_folder + '/y_val.pkl'})
                  config_dict.update({'x_val_path': newest_data_folder + '/x_val.pkl'})
                  
      elif ((~(os.path.exists(newest_data_folder + '/y_val.pkl'))) and (save_new_data_flag == 0) and (len(y_val) == 0)):
          pass
      else:
          save_new_data_flag = 1


      if (os.path.exists(newest_data_folder + '/y_test.pkl')) and (save_new_data_flag == 0) and (len(y_test) > 0):
          percent_20 = int((20/100)*len(y_test))

          with open(newest_data_folder + '/y_test.pkl', 'rb') as f:
              x = dill.load(f)

              if not np.array_equal(x[:percent_20], y_test[:percent_20]):
                  save_new_data_flag = 1
              else:
                  config_dict.update({'y_test_path': newest_data_folder + '/y_test.pkl'})
                  config_dict.update({'x_test_path': newest_data_folder + '/x_test.pkl'})
                  
      elif ((~(os.path.exists(newest_data_folder + '/y_test.pkl'))) and (save_new_data_flag == 0) and (len(y_test) == 0)):
          pass
      else:
          save_new_data_flag = 1

  if save_new_data_flag == 1:

      temp = dataset_folder
      while os.path.exists(current_dir+'/data/'+temp):
          temp = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) + '-' + dataset_folder 

      dataset_folder = temp
      os.mkdir(current_dir+'/data/'+dataset_folder)

      if len(x_train) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/x_train.pkl', 'wb') as f:
            dill.dump(x_train, f, protocol=4)
        config_dict.update({'x_train_path': current_dir+'/data/'+dataset_folder+'/x_train.pkl'})

      if len(x_val) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/x_val.pkl', 'wb') as f:
            dill.dump(x_val, f, protocol=4)
        config_dict.update({'x_val_path': current_dir+'/data/'+dataset_folder+'/x_val.pkl'})

      if len(x_test) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/x_test.pkl', 'wb') as f:
            dill.dump(x_test, f, protocol=4)
        config_dict.update({'x_test_path': current_dir+'/data/'+dataset_folder+'/x_test.pkl'})


      if len(y_train) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/y_train.pkl', 'wb') as f:
            dill.dump(y_train, f, protocol=4)
        config_dict.update({'y_train_path': current_dir+'/data/'+dataset_folder+'/y_train.pkl'})

      if len(y_val) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/y_val.pkl', 'wb') as f:
            dill.dump(y_val, f, protocol=4)
        config_dict.update({'y_val_path': current_dir+'/data/'+dataset_folder+'/y_val.pkl'})


      if len(y_test) > 0:
        with open(current_dir+'/data/'+dataset_folder+'/y_test.pkl', 'wb') as f:
            dill.dump(y_test, f, protocol=4)
        config_dict.update({'y_test_path': current_dir+'/data/'+dataset_folder+'/y_test.pkl'})

      print("Dataset Directory: " + current_dir+"/data/"+dataset_folder)
  else:
      print("The current datasets are already saved locally at "+ newest_data_folder + ".")


  config_dict.update({'library': 'NumPy'})
  if (first_sweep_run == True) and (sweep_global == True):
    first_sweep_run = False

  data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': uname, 'key': ky}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)

  #dataset_dict = config_dict



def torch_dataloader(train=None, val=None, test=None, name="dataset", label_index=1, if_sweep_save_once = True, run_id = None):

  if disable == False:
    print("Mynacode disabled. To enable, set mynacode.disable(False)")
    return

  if auth_failed == True:
    print("Please login using mynacode.login(Username, Key) before calling mynacode.torch_data()")
    return

  global first_sweep_run
  train_labels_list = []


  if (if_sweep_save_once == True) and (first_sweep_run == False) and (sweep_global == True):
    print("Dataset saved on first run. Subsequent calls to the 'data()' function within the current sweep will be ignored.")
    return

  config_dict = {}

  if project_dir_global == "":
    print("Please run mynacode.start(...) before calling this function")
    return
  current_dir = project_dir_global

  if run_id_global == "":
    print("Please run mynacode.init(...) to initialize a run before calling this function")
    return

  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  name = name.replace("-", "")

  if sweep_global == True:
      dataset_folder = "S"+str(run_id_global)+"-"+name
  else:
      dataset_folder = "R"+str(run_id_global)+"-"+name

  # Check latest dataset folder
  save_new_data_flag = 0
  newest_data_folder = newest(current_dir+'/data')

  if newest_data_folder == None:
      save_new_data_flag = 1
  elif re.split(r'[\\/]', newest_data_folder)[-1].split('-')[-1] != name:
      save_new_data_flag = 1
  else:
      if (train != None) and (len(train) > 0) and (os.path.exists(newest_data_folder + '/train_dataloader.pkl')): #Both exist

          with open(newest_data_folder + '/train_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(train))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]

              if not np.array_equal(b1, b2):
                  print('Train dataloaders not same')
                  save_new_data_flag = 1
              else:
                  config_dict.update({'train_dataloader_path': newest_data_folder + '/train_dataloader.pkl'})
      elif (~(os.path.exists(newest_data_folder + '/train_dataloader.pkl'))) and (train == None): #Both don't exist
          pass
      else: #One exists, one doesn't
          save_new_data_flag = 1

      if ((os.path.exists(newest_data_folder + '/val_dataloader.pkl')) and (save_new_data_flag == 0) and (val != None) and (len(val) > 0)):
          with open(newest_data_folder + '/val_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(val))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]

              if not np.array_equal(b1, b2):
                  print('Val dataloaders not same')
                  save_new_data_flag = 1
              else:
                  config_dict.update({'val_dataloader_path': newest_data_folder + '/val_dataloader.pkl'})
      elif ((~(os.path.exists(newest_data_folder + '/val_dataloader.pkl'))) and (save_new_data_flag == 0) and (val == None)):
          pass
      else:
          save_new_data_flag = 1


      if (os.path.exists(newest_data_folder + '/test_dataloader.pkl')) and (save_new_data_flag == 0) and (test != None) and (len(test) > 0):
          with open(newest_data_folder + '/test_dataloader.pkl', 'rb') as f:
              x = dill.load(f)
              torch.manual_seed(0)
              b1 = next(iter(test))[label_index]
              torch.manual_seed(0)
              b2 = next(iter(x))[label_index]

              if not np.array_equal(b1, b2):
                  print('Test dataloaders not same')
                  save_new_data_flag = 1
              else:
                  config_dict.update({'test_dataloader_path': newest_data_folder +'/test_dataloader.pkl'})
      elif ((~(os.path.exists(newest_data_folder + '/test_dataloader.pkl'))) and (save_new_data_flag == 0) and (test == None)):
          pass
      else:
          save_new_data_flag = 1

  if save_new_data_flag == 1:

      temp = dataset_folder
      while os.path.exists(current_dir+'/data/'+temp):
          temp = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) + '-' + dataset_folder

      dataset_folder = temp
      os.mkdir(current_dir+'/data/'+dataset_folder)


      #print("To log the label count as an optional feature, the DataLoaders dataset should have a 'targets' attribute.")

      if train:

        with open(current_dir+'/data/'+dataset_folder+'/train_dataloader.pkl', 'wb') as f:
            dill.dump(train, f, protocol=4)
        config_dict.update({'train_dataloader_path': current_dir+'/data/'+dataset_folder+'/train_dataloader.pkl'})

      if val:
        with open(current_dir+'/data/'+dataset_folder+'/val_dataloader.pkl', 'wb') as f:
            dill.dump(val, f, protocol=4)
        config_dict.update({'val_dataloader_path': current_dir+'/data/'+dataset_folder+'/val_dataloader.pkl'})

      if test:
        with open(current_dir+'/data/'+dataset_folder+'/test_dataloader.pkl', 'wb') as f:
            dill.dump(test, f,protocol=4)
        config_dict.update({'test_dataloader_path': current_dir+'/data/'+dataset_folder+'/test_dataloader.pkl'})


      print("Dataset Directory: " + current_dir+"/data/"+dataset_folder)
  else:
      print("The current datasets are already saved locally at "+ newest_data_folder + ".")

  if (first_sweep_run == True) and (sweep_global == True):
    first_sweep_run = False

  config_dict.update({'library': 'PyTorch'})

  data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': uname, 'key': ky}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)
  #dataset_dict = config_dict



def tf_dataset(train=None, val=None, test=None, name="dataset", label_index=1, if_sweep_save_once = True, run_id = None):

  if disable == False:
    print("Mynacode disabled. To enable, set mynacode.disable(False)")
    return

  if auth_failed == True:
    print("Please login using mynacode.login(Username, Key) before calling mynacode.tensorflow_data()")
    return

  global first_sweep_run
  train_labels_list = []


  if (if_sweep_save_once == True) and (first_sweep_run == False) and (sweep_global == True):
    print("Dataset saved on first run. Subsequent calls to the 'data()' function within the current sweep will be ignored.")
    return

  config_dict = {}

  if project_dir_global == "":
    print("Please run mynacode.start(...) before calling this function")
    return
  current_dir = project_dir_global

  if run_id_global == "":
    print("Please run mynacode.init(...) to initialize a run before calling this function")
    return

  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  name = name.replace("-", "")

  if sweep_global == True:
      dataset_folder = "S"+str(run_id_global)+"-"+name
  else:
      dataset_folder = "R"+str(run_id_global)+"-"+name


  save_new_data_flag = 0
  newest_data_folder = newest(current_dir+'/data')

  if newest_data_folder == None:
      save_new_data_flag = 1
  elif re.split(r'[\\/]', newest_data_folder)[-1].split('-')[-1] != name:
      save_new_data_flag = 1
  else:
      if (train != None) and (len(train) > 0) and (os.path.exists(newest_data_folder + '/train_dataset.pkl')): #Both exist
          x = tf.data.Dataset.load(newest_data_folder + '/train_dataset.pkl')

          np.random.seed(0)
          for batch in x:
              b1 = batch[label_index]
              break

          np.random.seed(0)
          for batch in train:
              b2 = batch[label_index]
              break

          if not np.array_equal(b1, b2):
              save_new_data_flag = 1
          else:
              config_dict.update({'train_dataset_path': newest_data_folder + '/train_dataset.pkl'})
              
      elif (~(os.path.exists(newest_data_folder + '/train_dataset.pkl'))) and (train == None): #Both don't exist
          pass
      else: #One exists, one doesn't
          save_new_data_flag = 1

      if ((os.path.exists(newest_data_folder + '/val_dataset.pkl')) and (save_new_data_flag == 0) and (val != None) and (len(val) > 0)):
          x = tf.data.Dataset.load(newest_data_folder + '/val_dataset.pkl')
          np.random.seed(0)
          for batch in x:
              b1 = batch[label_index]
              break

          np.random.seed(0)
          for batch in val:
              b2 = batch[label_index]
              break

          if not np.array_equal(b1, b2):
              save_new_data_flag = 1
          else:
              config_dict.update({'val_dataset_path': newest_data_folder + '/val_dataset.pkl'})
              
      elif ((~(os.path.exists(newest_data_folder + '/val_dataset.pkl'))) and (save_new_data_flag == 0) and (val == None)):
          pass
      else:
          save_new_data_flag = 1


      if (os.path.exists(newest_data_folder + '/test_dataset.pkl')) and (save_new_data_flag == 0) and (test != None) and (len(test) > 0):
          x = tf.data.Dataset.load(newest_data_folder + '/test_dataset.pkl')
          np.random.seed(0)
          for batch in x:
              b1 = batch[label_index]
              break

          np.random.seed(0)
          for batch in test:
              b2 = batch[label_index]
              break

          if not np.array_equal(b1, b2):
              save_new_data_flag = 1
          else:
              config_dict.update({'test_dataset_path': newest_data_folder + '/test_dataset.pkl'})
              
      elif ((~(os.path.exists(newest_data_folder + '/test_dataset.pkl'))) and (save_new_data_flag == 0) and (test == None)):
          pass
      else:
          save_new_data_flag = 1

  if save_new_data_flag == 1:

      temp = dataset_folder
      while os.path.exists(current_dir+'/data/'+temp):
          temp = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)) + '-' + dataset_folder

      dataset_folder = temp
      os.mkdir(current_dir+'/data/'+dataset_folder)

      if train:
        tf.data.Dataset.save(train, current_dir+'/data/'+dataset_folder +'/train_dataset.pkl')
        config_dict.update({'train_dataset_path': current_dir+'/data/'+dataset_folder +'/train_dataset.pkl'})

      if val:
        tf.data.Dataset.save(val, current_dir+'/data/'+dataset_folder +'/val_dataset.pkl')
        config_dict.update({'val_dataset_path': current_dir+'/data/'+dataset_folder +'/val_dataset.pkl'})

      if test:
        tf.data.Dataset.save(test, current_dir+'/data/'+dataset_folder +'/test_dataset.pkl')
        config_dict.update({'test_dataset_path': current_dir+'/data/'+dataset_folder +'/test_dataset.pkl'})

      config_dict.update({'prev_saved_data': False})
      print("Dataset Directory: " + current_dir+"/data/"+dataset_folder)
  else:
      print("The current datasets are already saved locally at "+ newest_data_folder + ".")
      config_dict.update({'prev_saved_data': True})

  if (first_sweep_run == True) and (sweep_global == True):
    first_sweep_run = False

  config_dict.update({'library': 'Tensorflow'})

  data = {'run_id' : run_id_global, 'config_dict': str(config_dict), 'node_name': "Datasets", 'username': uname, 'key': ky}

  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)

'''
try:
  class MynacodeCallback(keras.callbacks.Callback):

      def __init__(self, metric_name, goal='maximize', name='best_model_chkpt', track={}, run_id=None):

          if disable == False:
            print("Mynacode disabled. To enable, set mynacode.disable(False)")
            return

          if auth_failed == True:
            print("Please login using mynacode.login(Username, Key) before calling MynacodeCallback()")
            return

          if run_dir_global == "":
            print("Please run mynacode.init(...) to create a run before calling this function")
            return

          self.metric_name = metric_name
          self.goal = goal
          self.run_id = run_id
          self.best_model = None
          self.best_metric_value = 0
          self.best_metric_epoch = 0
          self.save_model = False
          self.track_config = track
          self.name = name




      def on_train_end(self, logs=None):

          if disable == False:
            print("Mynacode disabled. To enable, set mynacode.disable(False)")
            return

          if auth_failed == True:
            print("Please login using mynacode.login(Username, Key) before calling MynacodeCallback()")
            return

          if run_dir_global == "":
            print("Please run mynacode.init(...) to create a run before calling this function")
            return

          global metric_values
          global index_count

          print("Model Directory: "+run_dir_global+'/model')

          index_count = 0
          metric_values = []


      def on_epoch_end(self, epoch, logs=None):

          if disable == False:
            print("Mynacode disabled. To enable, set mynacode.disable(False)")
            return

          if auth_failed == True:
            print("Please login using mynacode.login(Username, Key) before calling MynacodeCallback()")
            return

          if run_dir_global == "":
            print("Please run mynacode.init(...) to create a run before calling this function")
            return
        
          global metric_values
          global index_count
          global prev_min
          global prev_max
          results_dict = {}


          if self.metric_name not in logs.keys():
            print(self.metric_name + ' not found in log keys')
            keys = list(logs.keys())
            print("End epoch {} of training; got log keys: {}".format(epoch, keys))
          else:
            metric_values.append(logs.get(self.metric_name))
            
            if self.goal == 'maximize':
              if logs.get(self.metric_name) > prev_max:
                prev_max = logs.get(self.metric_name)
                results_dict.update({'metric_name': self.metric_name})
                results_dict.update({'metric_goal': 'maximize'})
                results_dict.update({'best_'+self.metric_name: logs.get(self.metric_name)})
                results_dict.update({'best_metric_index': index_count})
                results_dict.update({'best_'+self.metric_name+'_epoch': epoch})

                if not os.path.exists(run_dir_global+'/model'):
                  os.mkdir(run_dir_global+'/model')

                for filename in os.listdir(run_dir_global+'/'):
                  if filename.endswith('.hdf5'):
                    file_path = os.path.join(run_dir_global+'/', filename)
                    os.remove(file_path)

                self.model.save(run_dir_global+'/'+self.name+'.hdf5')
                
                with open(run_dir_global+'/best_model_logs.txt', 'w') as f:
                  f.write('Metric: '+ str(results_dict['metric_name']))
                  f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
                  f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch']))

                model_dict = {'library':'Keras', 'metric_values': metric_values,
                                    'best_model_path': run_dir_global+'/'+self.name+'.hdf5',
                                    'best_model_logs_path': run_dir_global+'/best_model_logs.txt',}

                config_dict = {**model_dict, **results_dict, **self.track_config}

                results(results_dict = config_dict, run_id = None)
              else:
                results(results_dict = {'metric_values': metric_values}, run_id = None)

            elif self.goal == 'minimize':
              if logs.get(self.metric_name) < prev_min:
                prev_min = logs.get(self.metric_name)
                results_dict.update({'metric_name': self.metric_name})
                results_dict.update({'metric_goal': 'minimize'})
                results_dict.update({'best_'+self.metric_name: logs.get(self.metric_name)})
                results_dict.update({'best_metric_index': index_count})
                results_dict.update({'best_'+self.metric_name+'_epoch': epoch})

                if not os.path.exists(run_dir_global+'/model'):
                  os.mkdir(run_dir_global+'/model')

                for filename in os.listdir(run_dir_global+'/'):
                  if filename.endswith('.hdf5'):
                    file_path = os.path.join(run_dir_global+'/', filename)
                    os.remove(file_path)

                self.model.save(run_dir_global+'/'+self.name+'.hdf5')
                
                with open(run_dir_global+'/best_model_logs.txt', 'w') as f:
                  f.write('Metric: '+ str(results_dict['metric_name']))
                  f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
                  f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch']))

                model_dict = {'library':'Keras', 'metric_values': metric_values,
                                    'best_model_path': run_dir_global+'/'+self.name+'.hdf5',
                                    'best_model_logs_path': run_dir_global+'/best_model_logs.txt',}

                config_dict = {**model_dict, **results_dict, **self.track_config}

                results(results_dict = config_dict, run_id = None)
              else:
                results(results_dict = {'metric_values': metric_values}, run_id = None)

            index_count += 1
            

except:
  pass
'''

try:
  class MynacodeCallback(keras.callbacks.Callback):

      def __init__(self, metric_name, goal='maximize', name='best_model_chkpt', track={}, run_id=None):

          if disable == False:
            print("Mynacode disabled. To enable, set mynacode.disable(False)")
            return

          if auth_failed == True:
            print("Please login using mynacode.login(Username, Key) before calling MynacodeCallback()")
            return

          if run_dir_global == "":
            print("Please run mynacode.init(...) to create a run before calling this function")
            return

          self.metric_name = metric_name
          self.goal = goal
          self.run_id = run_id
          self.best_model = None
          self.best_metric_value = 0
          self.best_metric_epoch = 0
          self.save_model = False
          self.track_config = track
          self.count = 0
          self.name = name

      def on_train_end(self, logs=None):

          self.count += 1
          run_reset()

      def on_epoch_end(self, epoch, logs=None):

          if disable == False:
            print("Mynacode disabled. To enable, set mynacode.disable(False)")
            return

          if auth_failed == True:
            print("Please login using mynacode.login(Username, Key) before calling MynacodeCallback()")
            return

          if run_dir_global == "":
            print("Please run mynacode.init(...) to create a run before calling this function")
            return
        
          global prev_min
          global prev_max
          results_dict = {}


          if self.metric_name not in logs.keys():
            print(self.metric_name + ' not found in log keys')
            keys = list(logs.keys())
            print("End epoch {} of training; got log keys: {}".format(epoch, keys))
          else:
            
            if self.goal == 'maximize':
              if logs.get(self.metric_name) > prev_max:
                prev_max = logs.get(self.metric_name)
                results_dict.update({'metric_name': self.metric_name})
                results_dict.update({'metric_goal': 'maximize'})
                results_dict.update({'best_'+self.metric_name: logs.get(self.metric_name)})
                results_dict.update({'best_'+self.metric_name+'_epoch': epoch})

                if not os.path.exists(run_dir_global+'/model'):
                  os.mkdir(run_dir_global+'/model')

                for filename in os.listdir(run_dir_global+'/'):
                  if filename.endswith('.hdf5'):
                    file_path = os.path.join(run_dir_global+'/', filename)
                    os.remove(file_path)

                self.model.save(run_dir_global+'/'+str(self.name+str(self.count))+'.hdf5')
                
                with open(run_dir_global+'/best_model_logs.txt', 'a') as f:
                  f.write('\nModel Name: '+ str(self.name+str(self.count))+'.hdf5'))
                  f.write('\Metric: '+ str(results_dict['metric_name']))
                  f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
                  f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch'])+'\n')

                model_dict = {'library':'Keras', 'metric_values': metric_values,
                                    'best_model_path': run_dir_global+'/'+self.name+'.hdf5',
                                    'best_model_logs_path': run_dir_global+'/best_model_logs.txt',}

                config_dict = {**model_dict, **results_dict, **self.track_config}

                results(results_dict = config_dict, run_id = None)

            elif self.goal == 'minimize':
              if logs.get(self.metric_name) < prev_min:
                prev_min = logs.get(self.metric_name)
                results_dict.update({'metric_name': self.metric_name})
                results_dict.update({'metric_goal': 'minimize'})
                results_dict.update({'best_'+self.metric_name: logs.get(self.metric_name)})
                results_dict.update({'best_'+self.metric_name+'_epoch': epoch})

                if not os.path.exists(run_dir_global+'/model'):
                  os.mkdir(run_dir_global+'/model')

                for filename in os.listdir(run_dir_global+'/'):
                  if filename.endswith('.hdf5'):
                    file_path = os.path.join(run_dir_global+'/', filename)
                    os.remove(file_path)

                self.model.save(run_dir_global+'/'+str(self.name+str(self.count))+'.hdf5')
                
                with open(run_dir_global+'/best_model_logs.txt', 'a') as f:
                  f.write('\nModel Name: '+ str(self.name+str(self.count))+'.hdf5'))
                  f.write('\Metric: '+ str(results_dict['metric_name']))
                  f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
                  f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch'])+'\n')

                model_dict = {'library':'Keras', 'metric_values': metric_values,
                                    'best_model_path': run_dir_global+'/'+self.name+'.hdf5',
                                    'best_model_logs_path': run_dir_global+'/best_model_logs.txt',}

                config_dict = {**model_dict, **results_dict, **self.track_config}

                results(results_dict = config_dict, run_id = None)
            

except:
  pass

def keras_model(model=None, name='best_model_chkpt', metric_name=None, metric_value=None, epoch=None, track={}, run_id=None):

    if disable == False:
        print("Mynacode disabled. To enable, set mynacode.disable(False)")
        return

    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.torch_model()")
      return

    results_dict = {}

    if run_dir_global == "":
      print("Please run mynacode.init(...) to create a run before calling this function")
      return

    if model:

        results_dict.update({'metric_name': metric_name})
        results_dict.update({'best_'+metric_name: metric_value})
        results_dict.update({'best_'+metric_name+'_epoch': epoch})
        
        if not os.path.exists(run_dir_global+'/model'):
          os.mkdir(run_dir_global+'/model')

        for filename in os.listdir(run_dir_global+'/'):
          if ((filename.endswith('.hdf5')) and (filename not in saved_models)):
            file_path = os.path.join(run_dir_global+'/', filename)
            os.remove(file_path)

        model.save(run_dir_global+'/'+name+'.hdf5')

        with open(run_dir_global+'/best_model_logs.txt', 'a') as f:
          f.write('Metric: '+ str(results_dict['metric_name']))
          f.write('\nBest Value: ' + str(results_dict['best_'+str(results_dict['metric_name'])]))
          f.write('\nBest Epoch: ' + str(results_dict['best_'+str(results_dict['metric_name'])+'_epoch'])+'\n')

        model_dict = {'library':'Keras', 'metric_values': metric_values,
                            'best_model_path': run_dir_global+'/best_model_chkpt.hdf5',
                            'best_model_logs_path': run_dir_global+'/best_model_logs.txt',}

        config_dict = {**model_dict, **results_dict, **track}

        results(results_dict = config_dict, run_id = None)
    else:
        print("Please specify a keras model")
        return



@suppress_warnings
def results(y_true = [], y_pred = [], threshold=0.5, results_dict = {}, problem_type = 'binary classification', run_id = None):

    if disable == False:
      print("Mynacode disabled. To enable, set mynacode.disable(False)")
      return


    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.results()")
      return

    if not run_id:
      run_id = run_id_global

    if len(y_true) != 0 and len(y_pred) != 0:

      y_pred = np.array(y_pred).flatten()
      y_true = np.array(y_true).flatten()

      zero_idx = np.where(y_true == 0)[0]
      one_idx = np.where(y_true == 1)[0]

      prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_pred, threshold)
      fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_pred)

      fpr_spaced, tpr_spaced = evenly_spaced_points(fpr, tpr, 500)

      hist_zero = plt.hist(y_pred[zero_idx].tolist(), bins=30)
      hist_zero_freq = hist_zero[0]
      hist_zero_bins = hist_zero[1]

      hist_one = plt.hist(y_pred[one_idx].tolist(), bins=30)
      hist_one_freq = hist_one[0]
      hist_one_bins = hist_one[1]

      binary = {'precision': round(prec, 4), 'recall': round(rec, 4), 'specificity': round(spec, 4),
              'f1': round(f1, 4), 'accuracy': round(acc, 4), 'npv': round(npv_val, 4), 'c_matrix': c_matrix,
              'test_auc': roc_auc, 'hist_zero_freq': hist_zero_freq.tolist(), 'hist_zero_bins': hist_zero_bins.tolist(),
              'hist_one_freq': hist_one_freq.tolist(), 'hist_one_bins': hist_one_bins.tolist(),'fpr': fpr_spaced, 'tpr': tpr_spaced,
              'threshold': round(threshold, 4)}

      results_dict.update(binary)


      file=open(run_dir_global+"/results.yaml","w")
      yaml.dump({'precision': float(round(prec, 4)), 'recall': float(round(rec, 4)), 'specificity': float(round(spec, 4)),
                 'f1': float(round(f1, 4)), 'accuracy': float(round(acc, 4)), 'npv': float(round(npv_val, 4)),
                 'test_auc': float(roc_auc), 'threshold': float(round(threshold, 4))},file)
      file.close()

      preds_df = pd.DataFrame({'labels': y_true, 'predictions': y_pred})
      preds_df.to_csv(run_dir_global+'/predictions.csv', index=False)

    data = {'run_id' : run_id, 'results_dict': str(results_dict), 'node_name': 'Results', 'username': uname, 'key': ky}

    response = requests.post(protocol+'://'+IP+'/api/add_results', data=data)

    if response.text == '0':
      print("Authentication failed")


@suppress_warnings
def load(run_id = None, compute_results=False):
    if auth_failed == True:
      print("Please login using mynacode.login(Username, Key) before calling mynacode.results()")
      return

    data = {'run_id' : run_id, 'username': uname, 'key': ky}

    response = requests.post(protocol+'://'+IP+'/api/load_run', data=data)

    response_dict = ast.literal_eval(response.text)
    
    for key, value in response_dict.items():
        print(f'{key}: {value}')

    
    return_dict = {}

    if 'dataset_library' in response_dict:

        if response_dict['dataset_library'] == 'NumPy':
            if 'train' in response_dict:
              with open(response_dict['x_train'], "rb") as file:
                  train = dill.load(file)
                  return_dict.update({'x_train': train})
                  
            if 'val' in response_dict:
              with open(response_dict['x_val'], "rb") as file:
                  val = dill.load(file)
                  return_dict.update({'x_val': val})
                  
            if 'test' in response_dict:
              with open(response_dict['x_test'], "rb") as file:
                  test = dill.load(file)
                  return_dict.update({'x_test': test})
                  
            if 'y_train' in response_dict:
              with open(response_dict['y_train'], "rb") as file:
                  y_train = dill.load(file)
                  return_dict.update({'y_train': y_train})
                  
            if 'y_val' in response_dict:
              with open(response_dict['y_val'], "rb") as file:
                  y_val = dill.load(file)
                  return_dict.update({'y_val': y_val})
                  
            if 'y_test' in response_dict:
              with open(response_dict['y_test'], "rb") as file:
                  y_test = dill.load(file)
                  return_dict.update({'y_test': y_test})

        elif response_dict['dataset_library'] == 'PyTorch':
            if 'train_dataloader' in response_dict:
              with open(response_dict['train_dataloader'], "rb") as file:
                  train = dill.load(file)
                  return_dict.update({'train_dataloader': train})
                  
            if 'val_dataloader' in response_dict:
              with open(response_dict['val_dataloader'], "rb") as file:
                  val = dill.load(file)
                  return_dict.update({'val_dataloader': val})
                  
            if 'test_dataloader' in response_dict:
              with open(response_dict['test_dataloader'], "rb") as file:
                  test = dill.load(file)
                  return_dict.update({'test_dataloader': test})

        elif response_dict['dataset_library'] == 'Tensorflow':
            pass
        else:
            pass

        if 'val_thresh' in response_dict:
            return_dict.update({'val_thresh': response_dict['val_thresh']})
          
    if 'model_library' in response_dict:
        
        if response_dict['model_library'] == 'PyTorch':
            model_statedict = torch.load(response_dict['best_model_statedict'])
            with open(response_dict['best_model_network'], "rb") as file:
                model_network = dill.load(file)
            return_dict.update({'best_model_statedict': model_statedict, 'best_model_network': model_network})
            
        elif response_dict['model_library'] == 'Keras':
            model = tf.keras.models.load_model(model_path)
            return_dict.update({'best_model': model})

    if compute_results == True:
        
        print("\nLoading test data and model...")
        if response_dict['dataset_library'] == 'PyTorch':
            test_loader = return_dict['test_dataloader']
        if response_dict['model_library'] == 'PyTorch':
            Netx = return_dict['best_model_network']
            Netx.load_state_dict(return_dict['best_model_statedict'])

        print("Starting inference...")
        print("Note: You may need to manually import any necessary libraries and functions as required by your model.")

        toutput_list = []
        ttarget_list = []

        with torch.no_grad():
          for tbatch_idx, (tdata, ttarget) in enumerate(test_loader):
            toutput_list.append(Netx(tdata))
            ttarget_list.append(ttarget)

        y_pred = np.array(torch.cat(toutput_list)).flatten()
        y_true = np.array(torch.cat(ttarget_list)).flatten()

        zero_idx = np.where(y_true == 0)[0]
        one_idx = np.where(y_true == 1)[0]

        prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_pred, float(return_dict['val_thresh']))
        fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_pred)

        fpr_spaced, tpr_spaced = evenly_spaced_points(fpr, tpr, 500)

        hist_zero = plt.hist(y_pred[zero_idx].tolist(), bins=30)
        hist_zero_freq = hist_zero[0]
        hist_zero_bins = hist_zero[1]

        hist_one = plt.hist(y_pred[one_idx].tolist(), bins=30)
        hist_one_freq = hist_one[0]
        hist_one_bins = hist_one[1]

        binary = {'precision': round(prec, 4), 'recall': round(rec, 4), 'specificity': round(spec, 4),
              'f1': round(f1, 4), 'accuracy': round(acc, 4), 'npv': round(npv_val, 4), 'c_matrix': c_matrix,
              'test_auc': roc_auc, 'threshold': float(return_dict['val_thresh'])}

        print(binary)
        
        
        

    return return_dict
        

