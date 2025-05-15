# hcmut-multidisciplinary-project
# Intro
The project is inspired by smart home application where there are several smart features such as FaceID, Voice Control (currently availble for fan contraol and light control), and information of room Temperature, Humidity.

#Usage
## Frontend
The project can be run by localhost using:
```
cd frontend
npm install
npm start
```


## Backend
### Installation
For [**Window**](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
For [**Linux**](https://www.mongodb.com/docs/manual/administration/install-on-linux/)
For [**MacOS**](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)

To run back end, please download MongoDB first, then from the parent workspace:
```
cd backend
uvicorn src.__innit__:app --reload
```
