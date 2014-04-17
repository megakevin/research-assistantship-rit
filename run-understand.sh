#!/bin/bash

und create -db project_metrics -languages c++ java c# web python add /home/kevin/Desktop/repos/facebook-android-sdk

# Create the metrics-db for the tag
echo "> Creating the understand-db..."
und -db project_metrics settings -Metrics CountLine CountLineCode CountLineComment SumCyclomatic Cyclomatic CountDeclFunction CountDeclFile
und -db project_metrics settings -ReportReports "File Average Metrics" "Project Metrics" "File Metrics"
und -db project_metrics settings -MetricFileNameDisplayMode RelativePath

# Analyze the code
echo "> Analyzing the code..."
und -db project_metrics analyze &> /dev/null

# Create the csv file with the metrics
echo "> Getting the metrics..."
und -db project_metrics metrics
echo "> Storing the metrics into project_metrics_lol.csv..."
echo "Kind,Name,CountLine,CountLineCode,CountLineComment,SumCyclomatic,Cyclomatic,CountDeclFunction,CountDeclFile" > project_metrics_lol.csv
grep "File," project_metrics.csv >> project_metrics_lol.csv