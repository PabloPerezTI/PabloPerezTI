<img src="assets/hero.svg" width="100%" alt="Pablo Pérez, data engineer in Seville, Spain. Animated banner where raw data flows through bronze, silver and gold layers and comes out clean.">

**English** | [Español](README.es.md)

I'm a data engineer with three years in consulting, building PySpark pipelines for banking and insurance clients. Most of my work now happens on the Databricks lakehouse, with declarative pipelines, Unity Catalog, Delta Lake and Auto Loader running on AWS.

I enjoy the unglamorous parts that make data trustworthy: identity rules for sources that don't have keys, data quality checks that quarantine bad rows instead of silently dropping them, and lineage you can actually follow.

<img src="assets/about.svg" width="100%" alt="About me as a SQL query. Name: Pablo Pérez. Role: Data Engineer at Accenture. Based in Seville, Spain. Experience: 3 years across NTT Data, Izertis and Accenture. Works with PySpark, Databricks, Delta Lake and AWS. Building the Madrid Real Estate Lakehouse. Learning Lakebase and MLOps on Databricks. Speaks Spanish and English.">

## Featured work

<p>
  <a href="https://github.com/PabloPerezTI/real-estate-lakehouse"><img src="assets/project-lakehouse.svg" width="49%" alt="Madrid Real Estate Lakehouse: batch and streaming lakehouse on Databricks for an Idealista-style property portal"></a>
  <a href="https://github.com/PabloPerezTI/databricks-lakebase-tickets-app"><img src="assets/project-tickets.svg" width="49%" alt="Lakebase Tickets App: early prototype of a support ticket system on Databricks Apps and Lakebase"></a>
</p>

**[Madrid Real Estate Lakehouse](https://github.com/PabloPerezTI/real-estate-lakehouse)** is where I practise end-to-end platform work. It models about 21,000 real Madrid listings plus a stateful event simulator that lands price changes in S3. Bronze and silver run on Lakeflow Spark Declarative Pipelines and are governed in Unity Catalog, with a gold star schema coming next. The design notes explain each modelling decision, including the hash-derived property key for a source that has no natural one.

**[Lakebase Tickets App](https://github.com/PabloPerezTI/databricks-lakebase-tickets-app)** is an early prototype of a support ticket system built to run as a Databricks App. The data layer is in place: a Flask service connects to Lakebase (managed Postgres) through a secret scope and picks up user identity from the app's forwarded headers. The ticket endpoints are next.

## Stack

<img src="assets/stack.svg" width="100%" alt="Tech stack by pipeline stage. Ingest: Auto Loader, AWS Glue, AWS Lambda, Amazon EventBridge, Apache Kafka. Process: PySpark, Spark SQL, Declarative Pipelines, Python, pandas. Store and govern: Delta Lake, Unity Catalog, Amazon S3, Snowflake, PostgreSQL. Orchestrate: Lakeflow Jobs, Apache Airflow, Asset Bundles, Docker, GitHub Actions. Serve: Amazon Athena, Amazon QuickSight, Databricks Apps, Flask.">

## Certifications

<img src="assets/certs.svg" width="100%" alt="Certifications: AWS Certified Data Engineer Associate, Databricks Certified Data Engineer Associate, Databricks Certified Associate Developer for Apache Spark, Snowflake SnowPro Core.">

## Contributions

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/PabloPerezTI/PabloPerezTI/output/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/PabloPerezTI/PabloPerezTI/output/snake-light.svg">
  <img alt="Contribution graph being eaten by a snake, colored from bronze to gold by activity" src="https://raw.githubusercontent.com/PabloPerezTI/PabloPerezTI/output/snake-light.svg">
</picture>

## Get in touch

Happy to talk about lakehouse design, Databricks or anything data engineering. Email me at [pabloperezorti@gmail.com](mailto:pabloperezorti@gmail.com).

Outside the day job I co-founded [Meritia](https://meritia.es), a small business that sells NFC review stands, which is where I learned to ship things end to end.
