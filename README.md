python cost report

according my reseach i found someone else that already wrote the same project in python

https://github.com/hjacobs/aws-cost-and-usage-report

i made 3 changes.

  1. added region in args parse (now it posible to inject the region by argument)
  2. i removed the linked account column and now the table present the service name and the cost.
  3. set default profile to "default" instead of "dev"

required package: boto3

must access and secret key to aws with relevant permmision

to run the script please run the command:

python used_services.py --region us-east-1 --days 30

thanks

