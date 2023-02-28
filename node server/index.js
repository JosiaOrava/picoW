const express = require('express');
const mqtt = require('mqtt');
const path = require('path');
const util = require('util');
const fs = require('fs');
const bodyParser = require('body-parser');
const app = express();

const readFile = util.promisify(fs.readFile);
const writeFile = util.promisify(fs.writeFile);



app.use(bodyParser.json());
function read(filePath = './message.json') {
    return readFile(path.resolve(__dirname, filePath)).then(data => JSON.parse(data));
}
function write(data, filePath = './message.json') {
    return writeFile(path.resolve(__dirname, filePath), JSON.stringify(data));
}

// create an MQTT instance
const client = mqtt.connect('mqtt://192.168.1.254');
const title = 'josiaPico';

// Check that you are connected to MQTT and subscribe to a topic (connect event)
client.on('connect', () => {
    client.subscribe(title);
})

// handle instance where MQTT will not connect (error event)
client.on('error', (err) => {
    console.log('Error: ', err);
})
// Handle when a subscribed message comes in (message event)
client.on('message', async (topic, message) => {
    try{
        const messages = await read();
        console.log(messages);
        messages.push({"id": randomID(6), "msg": message.toString()});
        write(messages);
    } catch(e){
        console.log('Error: ' + e);
    }
})
// Route to serve the home page
app.get('/',(req,res) => {
    res.sendFile('index.html', {root: __dirname});
})

// route to serve the JSON array from the file message.json when requested from the home page
app.get('/messages', async (res,req) =>{
    let messages = await read();
    req.send(messages);
})
// Route to serve the page to add a message
app.get('/add', (req,res)=> {
    res.sendFile('message.html', {root: __dirname});
})
//Route to show a selected message. Note, it will only show the message as text. No html needed
app.get('/:id', async (req,res) => {
    const messages = await read();
    res.send(messages.filter(c => c.id === req.params.id));
})

// Route to CREATE a new message on the server and publish to mqtt broker
app.post('/', async (req,res) => {
    let title = req.body.topic;
    let msg = req.body.msg;
    try{
        client.publish(title, msg);
        res.sendStatus(200);
    } catch(e){
        console.log('Error: ' + e);
        res.sendStatus(200);
    }
    
})

// Route to delete a message by id

app.delete('/:id', async (req, res) => {
    try {
        const messages = await read();
        write(messages.filter(c => c.id !== req.params.id));
        res.sendStatus(200);
    } catch (e) {
        res.sendStatus(200);
    }
});

// Create random id for message
function randomID(length){
    let result = '';
    let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let charLength = chars.length;


    for ( let i = 0; i < length; i++ ) {
        result += chars.charAt(Math.floor(Math.random() * charLength));
    }
    return result;
}

// listen to the port
app.listen(3000);