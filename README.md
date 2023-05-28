# Hello-bot
1. Start the ec2 machine
2. Connect to the ec2 machine
3. Type 'minikube start'
4. On another browser tab connect to jenkins via ec2-Public IPv4:8080
5. From jenkins gui (section 4) run 'alon-bot-images' to build and push the images
6. Run 'alon-bot-deploy' to deploy all pods and services
7. Connect to the ec2 machine in another connection
7. In the new connection run the command 'kubectl get pods -n jenkins'
8. than run the command 'kubectl -n jenkins port-forward alon-bot-nginx-<generated no.> 8001:80'
9. Go back to the first ec2 connection and run 'curl http:127.0.0.10:8001'
