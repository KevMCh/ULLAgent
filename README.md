# _ULLAgent_

## Description

Chat bot using the google plataform to create bots
[DialogFlow](https://dialogflow.com/).

This bot is focused on providing information about the ULL in differents topics. The repository contain the webhook to connect with the selected APIs (news, calls and events).

## The server

This repository is in [Django](https://www.djangoproject.com/), and there are two apps.

On the one hand, the _chat_, a simple web page where you can deploy and tested the bot in a simple chat.

On the other hand, thes webhooks that connect to the defined APIs and respond to the agent.

## The agent

The _DialogFlowAgent_ folder contain the compress zip with the DialogFlow agent. You can import the agent to create it on the platform. This is the [documentation to import/export](https://dialogflow.com/docs/best-practices/import-export-for-versions) a agent.
