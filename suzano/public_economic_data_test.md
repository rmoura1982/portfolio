# Data Engineer Test

You are working in a project that uses public economic data to predict some directions regarding the paper price.

A Data Scientist in your project asks you to gather data from the **investing.com** website.

He needs the data from Chinese Caixin Services Index and USD/CNY **Daily**.

He gaves you website pages that you can get this information.

### Chinese Caixin Services Index

https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596

He said that the graph below has exact the information that he needs  monthly data from 2012 till today 
![image](https://user-images.githubusercontent.com/100236949/155219031-fd66bb59-b3f8-450f-9a7f-df1df35f70b7.png)

### USD/CNY

https://br.investing.com/currencies/usd-cny

He said that he needs monthly data from 1991 till now


## Goal
You need to build a code that gets the data in a automatic way and load the data in tables as below :

| Chinese Caixin Services Index | 
| :---:  |
|date | 
|actual_state | 
|close | 
|forecast | 

| USD/CNY  | 
| :---:  |
|date | 
|close | 
|open | 
|high | 
|low | 
|volume | 


## Closing Remarks
- Use the programming language of your choice (But we love Python, just a tip  i'm kidding it's up to you :D ).

- Use the libraries that are already built to make your work easier (remember in the end of the day what is important is the job done).

- Use a database to store the data in tables format (dont use SQLlite).

- Draw the architecture used and write a Readme file.

- **Seize this opportunity to demonstrate your skills in some data pipeline orchestration framework, containerization and cloud computing technology (preferably use terraform, gcp or airflow)!**

- Store your code in your Github account make it **private** or share it directly at our emails as zip file.


Good luck!
