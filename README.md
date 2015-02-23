# Social Media Harvester

The general purpose of SMH is to collect data from social media networks over a specific period of time in a geographic region with certain content. Most of the various social media networks provide endpoints that can supply you with the needed data, but if you want to get data from several networks you have to connect to every single API in a different manner. This can be very confusing and demanding. SMH offers an abstraction layer that takes parameters ones, translates them to their network specific equivalent and performs a request to every single API in the background.

## Creating a query
### Receive submitted request
The flow starts with receiving the request to create a new query. This request contains all parameters as key-value-pairs and a list of all selected harevsters with the key “selectedHarvesters”. The keys of parameters are structured in the following way: 
```
param_<harvester>_<paramName>
```

### Which harvesters are selected?
Get all the names of the selected harvesters from the query parameter 'selectedHarvesters' and save them to an array.

### Generate collection name
The harvesting scripts need to know where to save their data. Therefore a collection name is generated after the following scheme: `<username>_<current time>`

### Get meta parameters
Iterate over the parameters submitted in the request and search for the term 'param_meta' in the key. If it is found save the parameter to a meta  parameter dictionary with the name of the parameter (without 'param_meta_' prefix) as key.

### Start harvesting procedure
Then iterate over the list of selected harvesters and execute the following steps:
- Iterate over the parameter list and search for the harvester name in the parameter key. If it is found store the parameter in a dictionary with the name of the parameter (without prefix) as key.
- Get the mapping information from each harvester and search for the corresponding parameter in the global parameters submitted with the query (key: 'param_global..'). If found store the parameter to the parameter dictionary with the harvester specific name as key.
- Call startHarvesting(...)-method and pass the parameters and the meta parameters dictionary, the collection name and the user.

### Start Harvesting script
Inside the startHarvesting-method the harvesting script is started using subprocess.Popen(). The harvester parameters are passed to the script as options (`--track=test`).
The call returns the process id of the running script.

### Save query information to database
After starting the script new entries for the query and its parameters are created in the database. The database has the following scheme:


## Adding a new Harvester
Another key concept of SMH is its dynamic expandability. If there is a new social network from which the user wants to collect data it is possible to write a new harvester and integrate it into SMH. A list of things to consider when writing a new harvester is given in the document "Write your own Module".

On completing the development of a new harvester, three files are uploaded to the server. An executable script that does the harvesting, an icon that is displayed in the harvester selection and the specification file of the parameters the harvester accepts. The form for submitting these files is specified in `/database/forms.py`.

The request with whom the files are submitted is received inside the `uploadHarvester_view(request) – method of views.py`. There the `installModule(json_file, icon, script)` – method in `HarvesterToolkit.py` is called. This method performs the following steps:

1. write submitted files to /modules/<module> directory with method:
```
writeFileToDirectory(directory, file_data, file_name)
```

2. generate small greyish icon (displayed in the parameter fields)
```
generateSmallIcon(icon_big) NOT IMPLEMENTED YET
```

3. add modules to list of installed modules (installedModules.ini)
```
addModuleToInstalledModules(name, path_to_json_conf)
```

If the installing of the module fails at any point the installation should do a full rollback, which is sadly not implemented yet.

## From JSON to a Module class
To work with the installed modules and pass them for example to the front-end instances of the Module class are created. A module class provides methods such as startHarvesting(...) which starts the harvesting or `getParametersToDisplay()` which return the parameters that should be displayed in the front-end. The attribute of a Module object are populated from a JSON file. The following image shows what JSON entries are accessible through which attribute of the Module class. The same goes for a harvester parameter represented by a HarvesterParameter class.

An explanation for the different entries of the JSON file is given in the "Write Your Own Module" document.

## Displaying queries to the user
In the “My Queries” view the user can look at his own queries. Therefore he is sending a GET-request to the server which is handled in the method query_view(request) in /database/views.py. After receiving the request a lookup on the database is performed which returns only the queries that have the current user as their owner.

```
queries = models.query.objects.filter(owner=request.user)
```

Then another lookup is performed to get all the parameters which belong to the found queries.

```
parameters = models.parameter.objects.filter(query_id=q.id)
```

The queries an their parameters are then passed to the query.html template which is returned to the use.

## Checking for stoptime
A key aspect of SMH is the stoptime-parameter of every query. It specifies when a query should end. This means if the stoptime is passed the query has to be terminated as soon as possible. Therefore the 'query_checker.py' exists. The script is executed every 5 minutes via crontab. Editing crontabs is possible with

```
	crontab -e
```

The script performs a lookup on the database and checks if there are any queries which are marked as still running but have surpassed their stoptime. The script then tries to terminate the python process behind the query.
First it is checked if a process with the given id exists or not and if its running or  in a zombie state. If it is still running the method `ProcessKiller.kill_query(query)` is called and the query object retrieved from the database is passed to it. This method tries to kill the process with a `kill -9` command. If it was successful the database entry is updated. Also if the process does not exist or is already zombified the database entry is updated and isRunning is set to False.
To manually check if the process has terminated use the command line.

```
ps -ef (—forest)
```

If the process is terminated correctly it should not be displayed anymore or be named `[python] <defunct>`. A `defunct` zombie process is later terminated by some sort of garbage collector.

## Terminate running queries
If a query needs to be stopped before it has reached its stop-time this can be achieved in the “My Queries”-view by pressing on 'X'. This sends a request to the server with the pid of the queries process. The server then executes the method ProcessKiller.kill_pid(pid) which kills the process and leaves it zombified.
After killing the process an updated view is returned.

## Changing password
For the user it is possible to change his password. He can do so in the “Password”-view.  There he has to enter his old password and the new password which are then both submitted inside a request to the server.
There the request is handled by the method password_view(request).

## Logging
SMH provides a logging mechanism. It can be retrieved with:

```
import logging
log = logging.getLogger('smh')
```

Logging statements can than be printed with a logging level as follows:

```
log.info('')
log.debug('')
log.warning('')
log.error('')
log.critical('')
```

The logging statements printed with the above commands are written to `/logs/logfile.log`.
