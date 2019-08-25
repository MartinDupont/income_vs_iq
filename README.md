# income_vs_iq

This is an attempt to demonstrate the effect of IQ on income. Many commentators on the internet have attempted to show that IQ has a clear positive
effect on earnings. However, many simply take a linear regression of income vs. IQ, or perhaps they use log income. These approaches are slightly 
wrong, as linear regression assumes that the residuals (or, error in the fitted model) are normally distributed. Given that income is Pareto distributed, 
this assumption is rather wrong. Transforming to log-income does not help, as the log income is exponentially distributed, which despite being easier to manage, 
still breaks the assumptions of linear regression. 

So, I have instead created a method of fitting a linear equation when the residuals are expected to be pareto distributed. This derivation is certainly
not original, and it was mostly a free-time experiment. I have included a derivation of my formulas as a PDF in the math_explainer folder.

## Sources
I used the [NLSY79](https://www.bls.gov/nls/nlsy79.htm) dataset, which follows a cohort of people throughout their life, and crucially, tracks both income
and an IQ test administered to the initial subjects. The IQ test is the AFQT, which is an intelligence test administered by the military, which essentially measures IQ. 
The dataset is also publically available for download.

I use the same data preprocessing approach as [this](http://www.jsmp.dk/posts/2019-06-16-talebiq/) commentator, who also worked on the same dataset.
He averages income over multiple years in order to obtain a clearer signal, and adjusts the income for inflation. He also adjusts for the age at which
the AFQT test was taken, as teenagers have often not reached their final IQ yet. 

## Results
The algorithm works and can indeed fit the distribution. And, for any reasonable training parameters, it shows an increase in earnings with IQ. 

## Limitations

The dataset is limited in that the measurement income from wages and business are capped at a certain value at any given year. The maximum value 
increases every year, but is on the order of 300,000 - 400.-000. As income from wages and business are added together to give the total income, 
the total income in this dataset is artificially capped at ~800,000 dollars. As Pareto distributions have very fat tails, this will have an effect on the results. 
Furthermore, on plotting the data, it is visible that many respondents earn more than the maximum value, and there is visible clipping in the dataset.

Another difficulty was the difficulty in fitting very low incomes. To fit a pareto distribution, a minimum value must be given. Depending on the 
minimum value chosen for the model, the results varied wildly. For very low minimum incomes, say ~10,000, the fitted α coefficient of the distribution
could become less than 1, leading to an undefined mean income for some IQ brackets. Which is obviously false. This is probably due to the difficulty in correctly
reporting very low incomes

## Conclusions
The algorithm is stable and can indeed fit the distribution. And, for any reasonable training parameters, it shows an increase in earnings with IQ. However, due to the dataset it is very sensitive to the minimum income parameter, and the results cannot be trusted except to say that there is __some__ increase in income with IQ.
