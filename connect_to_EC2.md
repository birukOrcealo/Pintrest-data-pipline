#### bash comands to connect the clint matchine to EC2 instances  
- Run the following command to ensure your key is not publicly viewable.
```bash 
bash 
chmod 400 "0a0c9995b889-key-pair.pem" # replace 0a0c9995b889-key-pair.pem  with actuall file name 
```
- Connect to your instance using its Public DNS:ec2-54-173-183-37.compute-1.amazonaws.com for example

```bash 

ssh -i "0a0c9995b889-key-pair.pem" root@ec2-54-173-183-37.compute-1.amazonaws.com # replace 0a0c9995b889-key-pair.pem  with actuall file name
```