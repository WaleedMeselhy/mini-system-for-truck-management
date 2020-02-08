
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
```