import express, { json } from 'express';
import cors from 'cors';
import { exec, spawn } from 'child_process';
import { readFile } from 'fs/promises';

const updateInstagramPics = () => {
    exec('sh ./scripts/instagram.sh', (err, stdout, stderr) => {
        if (err) {
            console.log(err);
            return;
        }
        console.log(stdout);
        console.log(stderr)
    });
};

const app = express();

app.use(
    cors({
        origin: '*',
    })
);

app.use(express.static('public'));

app.get('/api/instagram', async (req, res) => {
    console.log('instagram');
    try {
        // const bash = spawn('bash', ['./scripts/instagram.sh'])
        // bash.stdout.on('data', (data) => console.log(data))
        const data = JSON.parse(await readFile('posts.json', 'utf-8'))
        const last_updated = new Date(data.last_updated)
        if (last_updated.getDay() != new Date().getDay()) updateInstagramPics()
        return res.status(200).json(data)
    } catch (error) {
        console.log(error);
    }
});

app.get('/api/youtube', () => {
    console.log('youtube');
});

app.post('/api/commisions', () => {
    console.log('commissions');
});

app.listen(3000, () => {
    console.log('server running');
});
