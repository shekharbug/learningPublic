
1. create flask project
2. Create Dockerfile
3. build container

docker build -t flask-app .

4. Start container

docker run -d -p 5000:5000 --name flask-test-container flask-app
