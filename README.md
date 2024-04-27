# patients-reservation

Part of initial recruitment test by Zi.Care, I was tasked to design schema and write the CRUD APIs for the topic patients reservation, where from a list of patients, each of them can book a reservation for a consultation and the reservation is based on the clinic slot/schedule availability, lastly the patient will get the queue number.


## Assumptions Made During Development

1. **User Registration Process:** gives the user the role `patient` by default. (Registering as `Admin` can **only** be done by existing admins)
2. **Doctor Registration Process:** can **only** be done by `admin` and **only** for reservation purposes not for directly interacting with the `patient` (therefore no login function available for `doctors`)
3. **Schedules:** each schedule **only** has one slot, hence the usage of `is_available` field.


## Personal Take

#### Contact Me

<img src="https://raw.githubusercontent.com/RevoU-FSSE-2/week-7-SherinOlivia/3dd7cdf0d5c9fc1828f0dfcac8ef2e9c057902be/assets/gmail-icon.svg" width="15px" background-color="none">[SOChronicle@gmail.com](mailto:SOChronicle@gmail.com)

<img src="https://raw.githubusercontent.com/RevoU-FSSE-2/week-7-SherinOlivia/3dd7cdf0d5c9fc1828f0dfcac8ef2e9c057902be/assets/gmail-icon.svg" width="15px" background-color="none">[SOlivia198@gmail.com](mailto:SOlivia198@gmail.com) 

[![Roo-Discord](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-discord.svg)](https://discord.com/users/shxdxr#7539)[![Roo-Instagram](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-instagram.svg)](https://instagram.com/shxdxr?igshid=MzRlODBiNWFlZA==)[![Roo-LinkedIn](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-linkedin-circled.svg)](https://www.linkedin.com/in/sherin-olivia-07311127a/)