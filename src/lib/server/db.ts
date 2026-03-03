import { MongoClient } from 'mongodb';
import { env } from '$env/dynamic/private';

let client: MongoClient;

export async function getDb() {
  if (!client) {
    client = new MongoClient(env.MONGODB_URI);
    await client.connect();
  }
  return client.db('kelvins_weekly');
}
