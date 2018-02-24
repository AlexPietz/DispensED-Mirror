# DispensED Website

### Assigning a drug to patient
Drugs from a predefined list can be assigned to each patient. Quantity of the drug and time are also required when adding a drug to a specific patient. 

### Reading the list of assigned drugs
It is assumed that the robot will distribute drugs every 15 minutes. The reading of the list of drugs to be distributed at a spedific time is done by making a request to:  

```
http://localhost:5000/dbread
```

As a result of the request, a JSON file is returned containing a list of patients and the corresponding drugs in the period of +/- 15 minutes from the time of the request. 

For example, if a drug is to be dispensed at 10:00, it will be included in the list returned by a request made in the period from 09:45 until 10:15. 

This way the robot will have this information in the case that it finished earlier or later than supposed to with the current distribution.
