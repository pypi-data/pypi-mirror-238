from __future__ import annotations

from dataclasses import dataclass
from logging import Logger

from slack_sdk import WebClient  # type: ignore

from .constants import COMMON_SLACK_CHANNEL_ID
from .templates import Template


@dataclass
class PMSlackLogger:
    bot_token: str
    send_to_slack: bool = True
    logger: Logger | None = None

    def __post_init__(self) -> None:
        self.client = WebClient(token=self.bot_token)

    def send_text_message(self, channel: str, text: str) -> None:
        if self.send_to_slack is False:
            if self.logger:
                self.logger.info(text)
            return

        self.client.chat_postMessage(channel=channel, text=text)

    def send_template_message(self, template: Template) -> None:
        if self.send_to_slack is False:
            if self.logger:
                self.logger.info(template.message)
            return

        self.client.chat_postMessage(
            channel=template.channel,
            blocks=template.blocks,
            text="Paket Mutfak",  # Slack'te gosterilmiyor fakat vermeyince uyari veriyor
        )

    def send_message_with_default_template(
        self, header: str, text: str, err_code: str = None, channel: str = COMMON_SLACK_CHANNEL_ID
    ) -> None:
        if self.send_to_slack is False:
            if self.logger:
                self.logger.info(header)
            return

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": header,
                    "emoji": True,
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": text},
            },
        ]

        if err_code:
            blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Error Code: {err_code}"},
                }
            )

        self.client.chat_postMessage(
            channel=channel,
            blocks=blocks,
            text="Paket Mutfak",
        )
