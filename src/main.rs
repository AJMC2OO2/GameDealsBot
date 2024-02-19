use app::app;
use dotenv::dotenv;

mod app;
mod commands;
mod new_posts;

type Error = Box<dyn std::error::Error + Send + Sync>;

#[tokio::main]
async fn main() -> Result<(), Error> {
    dotenv()?;
    app().await?;
    Ok(())
}
