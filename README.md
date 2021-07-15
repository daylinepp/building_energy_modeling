# Building Energy Modeling

### Project Status: [Active]
This capstone project will be completed to conclude the [Data Science Bootcamp][LighthouseLabs] at Lighthouse Labs.  

## Project Information
<details open>
<summary>Show/Hide</summary>

### Project Worklfow
<details>
<summary>Show/Hide</summary>

- exploratory data analysis & visualization
- data processing & cleaning
- time series forecasting
- supervised learning modeling
- model evaluation
- feature importance analysis
- data application deployment 
</details>

## Background
Energy Modeling for building design is commonplace nowadays. It is the analysis and simulation of various energy related systems such as HVAC, gas, water and lighting to learn about energy consumption, utility use and cost, and equipment life cycle analysis. It is also used to calculate payback periods of green energy solutions. There are hundreds of software packages capable of this kind of simulation; however, the work is not done once building design is complete.

Building Automation Systems (BAS) are becoming much more widely accepted as a necessity, especially for large commercial buildings. This goes hand-in-hand with energy modeling; for all of the decisions made in the design process the BAS provides a central access point to monitor and control energy related systems once they're up and running.

## Project Overview
Energy modeling is a fantastic tool, but this project aims to prove that there are stones left unturned in optimizing energy efficiency. Data is collected by individual components of the BAS at all times, and this means potential. There is a wide variety of factors that influence energy consumption, and although data is readily available for most of them, it is a challenge to amalgamate. However, once this is done we can begin to leverage the power of forecasting and machine learning. This will facilitate consumption forecasting, predicting consumption at any time, and identification of equipment with the highest impact on consumption.

### 1. Energy Consumption Forecasting
The purpose of forecasting is to use a limited number of data features to learn trends and seasonality. This can be taken one step further to produce a forecast of energy consumption for a given window into the future. The quality of the forecast can be determined by how well it fits the actual data from the year in which it is available.

Initially, a forecast is produced from energy consumption data itself and the time each value was recorded, between June 2020 and May 2021. Time creates an inherent order in the data, so training happens with data recorded throughout the year to generate a forecast in a short window thereafter.

Two more features are added to the forecast; outside air temperature and energy demand. This drastically improves the fit due to high correlations between the features. It is helpful to understand the improvements with additional features, as it shows how simple additions can drastically help the outcome. Data leakage was a concern at this stage; however, it is reasonable for energy demand data to be available from the BAS prior to the output of a consumption value. Of course, these two correlate very closely so it is no surprise that allowing the forecasting model to learn with demand data produces a forecast with an excellent fit.

### 2. Supervised Learning
Moving forward to a supervised learning problem was a logical next step, but this task could have been approached in multiple ways. I considered the following options:
- formulating the time series data as a supervised learning problem.
- removing the time dependancy in the data to create a standard machine learning task.

The former requires observations to be lagged to create sequences of the original data as observations, and this can get cumbersome in the multivariate case. This may be something worth trying, and you can find a detailed article of the process [here][TimeSeriesToSupervised], but it will be left for the future for now.

I thought the more interesting approach would be to eliminate the time dependancy, and create a model to predict energy consumption for any hour, given the data observations of various equipment in the building. All possible features were used in the model. Although the performance was quite good, with an $R^2$ score of just over 90%, the more interesting result was to extract the top 10 most important features.

At the end of the day, predicting consumption allows you to determine if it is within an expected reasonable range. If it is, no action is necessarily required; if it is not, hopefully you might be able to take some proactive measures to mitigate massive inefficiencies. It is much more interesting to be able to extract the most important features from the model, and look at them more closely to try to improve the system as a whole.

### 3. Feature Importance
Determining feature importance from the model is the part of this project that opens the door to providing real industry value down the road. There is convenient functionality in the mmodeling packages to perform this, but what to do next is not at all trivial.

The ultimate goal of this work would be to produce detailed information about each contributing factor to energy consumption. This would include information about peak demand; when does it occur monthly, weekly, daily and which pieces of equipment drive this. This can help prioritize the hardware further. Including things like eqiupment life span, maintenance intervals and associated costs, and overall efficiency would contribute to the ability and willingness to make changes in order to improve efficiency. Unfortunately, time constraints did not permit implementation of such a process. Regardless, it will not be so straightforward, but I plan to continue this work at a later date.
</details>

## Technologies
<details>
<summary>Show/Hide</summary>

* Python
* Pandas
* Prophet
* Sklearn
* PyCaret
* Streamlit
* AWS EC2
</details>

## External Materials
* [Capstone Demo Presentation][presentation]
* Forecasting Web App via Streamlit

## Collaboration
The raw data used in this project is proprietary, and therefore not available. However, you can find source code for all of the work completed within this repository. I would be happy to receive feedback, and to discuss possibilities for future work.

If you are interested in further discussion, you can feel free to contact me by **[email](mailto:daylin.epp@gmail.com)** or on **[LinkedIn][linkedin]**.

### Industry Contributor
![Simpson Controls](images/Logo.jpg)  

You can also reach out to Simpson Controls, the owner of the data used for this project.  
Contact: [Taylor Simpson](mailto:taylor@simpsoncontrols.com)

[presentation]: https://drive.google.com/file/d/1B14PmA7SQkcFQNq2UeA5Xk5CXL7FCK2g/view?usp=sharing
[linkedin]: https://www.linkedin.com/in/daylin-epp-62989760/
[LighthouseLabs]: https://www.lighthouselabs.ca/en/data-science-bootcamp
[Prophet]: https://facebook.github.io/prophet/docs/quick_start.html#python-api
[ExtraRegressors]: https://facebook.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html#additional-regressors
[ProphetCV]: https://facebook.github.io/prophet/docs/diagnostics.html
[TimeSeriesForecastExample]: https://github.com/srivatsan88/End-to-End-Time-Series
[TimeSeriesToSupervised]: https://machinelearningmastery.com/convert-time-series-supervised-learning-problem-python/