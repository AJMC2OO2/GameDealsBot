use crate::{app::Context, new_posts::new_posts, Error};

/// Show this help menu
#[poise::macros::command(slash_command, prefix_command)]
pub async fn help(
    ctx: Context<'_>,
    #[description = "Command to show help info"]
    #[autocomplete = "poise::builtins::autocomplete_command"]
    command: Option<String>,
) -> Result<(), Error> {
    poise::builtins::help(
        ctx,
        command.as_deref(),
        poise::builtins::HelpConfiguration {
            extra_text_at_bottom: "¡Me pican los cocos!",
            ..Default::default()
        },
    )
    .await?;
    Ok(())
}

/// Get the first `n` new posts
///
/// Enter `gd.get n` to get all new posts
#[poise::macros::command(slash_command, prefix_command)]
pub async fn get(
    ctx: Context<'_>,
    #[description = "Number of new posts"] n: Option<u8>,
) -> Result<(), Error> {
    for post in new_posts().await?.iter().take(n.unwrap_or(1) as usize) {
        ctx.say(post["data"]["url"].to_string()).await?;
        println!("Posted");
    }
    Ok(())
}

/// Get all new posts
///
/// Enter `gd.get_all` to get all new posts
#[poise::macros::command(slash_command, prefix_command, aliases("all"))]
pub async fn get_all(ctx: Context<'_>) -> Result<(), Error> {
    for post in new_posts().await?.iter().take(5) {
        ctx.say(post["data"]["url"].to_string()).await?;
        println!("Posted");
    }
    Ok(())
}
