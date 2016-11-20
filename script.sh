#!/bin/sh
while true
do
	scrapy crawl reddit
	python twitter_bot.py
	sleep 5m
done