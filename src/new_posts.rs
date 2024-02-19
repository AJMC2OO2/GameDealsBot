use std::env;

use reqwest::{header::USER_AGENT, Client};
use serde_json::Value;

use crate::Error;

async fn request_new_posts() -> Result<Value, Error> {
    let user_agent = env::var("USER_AGENT")?;
    let subreddit = env::var("SUBREDDIT")?;

    let source = format!("https://www.reddit.com/{subreddit}/new.json?sort=new");
    let client = Client::new();
    let res = client
        .get(source)
        .header(USER_AGENT, user_agent)
        .send()
        .await?;
    let json: Value = res.json().await?;

    Ok(json)
}

pub async fn new_posts() -> Result<Vec<Value>, Error> {
    let json = request_new_posts().await?;
    assert!(json["kind"] == "Listing");
    let posts = json["data"]["children"].as_array().unwrap().to_vec();

    Ok(posts)
}
