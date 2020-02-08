
# mini system for truck management

The trips are just a sequential collection of objects points with the following models

# technologies used


**Celery & Rabbitmq** schedule jobs to calculates a daily report

**Flask**  for rest endpoints

**SQLAlchemy** as Object Relational Mapper

**Alembic** for databse migration


### Example

requires [Docker Compose](https://docs.docker.com/compose/) to run.

### Run example.


``` sh
git clone git@github.com:WaleedMeselhy/mini-system-for-truck-management.git
cd mini-system-for-truck-management
sudo ./run.sh # to run example
# press D at any time to stop
# every 30 seconds task will run to calculate all trucks activities
# example truck_id: 3, total_distance: 2100.24977709602, total_active_time: 0.031821999999999996


# in another terminal
start_timestamp=$(date +%s)

# add trucks
curl -X POST \
  http://localhost:5000/v1/truck/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 4402b4f9-0aa2-a3bb-cb84-b5f440d940c2' \
  -d '{
"plate_number":"test1"	
}'
curl -X POST \
  http://localhost:5000/v1/truck/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: b1193f4c-c0fc-2e85-aa26-3738ed4bed74' \
  -d '{
"plate_number":"test2"	
}'
curl -X POST \
  http://localhost:5000/v1/truck/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: c3e56a64-1067-949c-68ba-f62f8891fd38' \
  -d '{
"plate_number":"test3"	
}'


#add trucklogs for 1
curl -X POST \
  http://localhost:5000/v1/truck/1/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 9156d6b8-7c48-c280-d53d-0e82ca13115e' \
  -d '{
	
	"latitude": 37.773972,
	"longitude":  -122.43129
}'
curl -X POST \
  http://localhost:5000/v1/truck/1/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 0619a062-2dac-f7a3-183d-33f6eb61de64' \
  -d '{
	
	"latitude": 47.608013,
	"longitude":  -122.335167
}'
curl -X POST \
  http://localhost:5000/v1/truck/1/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: b81cac86-3fe8-e381-1cb4-ad02b7006827' \
  -d '{
	
	"latitude": 38.575764,
	"longitude":  -121.478851
}'
#add trucklogs for 2
curl -X POST \
  http://localhost:5000/v1/truck/2/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 9156d6b8-7c48-c280-d53d-0e82ca13115e' \
  -d '{
	
	"latitude": 37.773972,
	"longitude":  -122.43129
}'
curl -X POST \
  http://localhost:5000/v1/truck/2/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 0619a062-2dac-f7a3-183d-33f6eb61de64' \
  -d '{
	
	"latitude": 47.608013,
	"longitude":  -122.335167
}'
curl -X POST \
  http://localhost:5000/v1/truck/2/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: b81cac86-3fe8-e381-1cb4-ad02b7006827' \
  -d '{
	
	"latitude": 38.575764,
	"longitude":  -121.478851
}'
#add trucklogs for 3
curl -X POST \
  http://localhost:5000/v1/truck/3/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 9156d6b8-7c48-c280-d53d-0e82ca13115e' \
  -d '{
	
	"latitude": 37.773972,
	"longitude":  -122.43129
}'
curl -X POST \
  http://localhost:5000/v1/truck/3/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 0619a062-2dac-f7a3-183d-33f6eb61de64' \
  -d '{
	
	"latitude": 47.608013,
	"longitude":  -122.335167
}'
curl -X POST \
  http://localhost:5000/v1/truck/3/log \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: b81cac86-3fe8-e381-1cb4-ad02b7006827' \
  -d '{
	
	"latitude": 38.575764,
	"longitude":  -121.478851
}'
#get active trucks
curl -X GET \
  http://localhost:5000/v1/trucks 

end_timestamp=`expr $(date +%s) + 100`
#get summary 
curl "http://localhost:5000/v1/truck/1/summary?start_time=${start_timestamp}&end_time=${end_timestamp}"
```

