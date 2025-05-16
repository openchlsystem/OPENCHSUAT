#!/bin/bash
# wait-for-db.sh

# Set the MySQL hostname and port
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_USER=uat_user
MYSQL_PASSWORD=$MYSQL_PASSWORD

# Wait until MySQL is ready to accept connections
until mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1" > /dev/null 2>&1; do
  echo "Waiting for MySQL at $MYSQL_HOST:$MYSQL_PORT..."
  sleep 5
done

echo "Database is ready, starting backend!"
exec "$@"  # This will execute the original command (runserver)
