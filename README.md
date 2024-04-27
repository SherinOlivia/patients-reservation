# patients-reservation

Part of initial recruitment test by Zi.Care, I was tasked to design schema and write the CRUD APIs for the topic patients reservation, where from a list of patients, each of them can book a reservation for a consultation and the reservation is based on the clinic slot/schedule availability, lastly the patient will get the queue number.

## Database Schema

## How to Set Up

To Start the patients-reservation APIs locally, follow these steps:

1. Clone this repository to your local machine:

```bash
git clone https://github.com/SherinOlivia/patients-reservation.git
```

2. Navigate into the project directory:

```bash
cd patients-reservation
```

3. Open it in VSCode or any other of your choice:

```bash
code .
```
4. Install The Dependencies:

```bash
pipenv install
```

5. Run the Server:

```bash
uvicorn main:app --reload
```

6. Test the APIs through Postman. by using this link as the base and check the next part (Endpoint List):

```bash
http://localhost:8000/
```
or

8. Or access the documentation provided by fastapi:
[here](http://localhost:8000/docs)

## Assumptions Made During Development

1. **Users:** 
- registration process gives the user the role `patient` by default.
- registering as `admin` can **only** be done by existing admins
2. **Doctors:** 
- Doctor registrations can **only** be done by `admin` and **only** for reservation purposes not for directly interacting with the `patient` (therefore no login function available for `doctors`)
3. **Schedules:** 
- each schedule **only** has one slot, hence the usage of `is_available` field.
- `admin` can update the current date's schedules to new date instead of creating new schedules daily
- `admin` can manually update the availability of each schedule
4. **Reservations:** 
- resets **by date** instead of hourly
- **cannot** book reservations on schedules with **same date and time** even if by different doctors

## Personal Take

#### Contact Me

<img src="https://raw.githubusercontent.com/RevoU-FSSE-2/week-7-SherinOlivia/3dd7cdf0d5c9fc1828f0dfcac8ef2e9c057902be/assets/gmail-icon.svg" width="15px" background-color="none">[SOChronicle@gmail.com](mailto:SOChronicle@gmail.com)

<img src="https://raw.githubusercontent.com/RevoU-FSSE-2/week-7-SherinOlivia/3dd7cdf0d5c9fc1828f0dfcac8ef2e9c057902be/assets/gmail-icon.svg" width="15px" background-color="none">[SOlivia198@gmail.com](mailto:SOlivia198@gmail.com) 

[![Roo-Discord](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-discord.svg)](https://discord.com/users/shxdxr#7539)[![Roo-Instagram](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-instagram.svg)](https://instagram.com/shxdxr?igshid=MzRlODBiNWFlZA==)[![Roo-LinkedIn](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-linkedin-circled.svg)](https://www.linkedin.com/in/sherin-olivia-07311127a/)