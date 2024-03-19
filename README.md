# CMP408-Nordpi
Nordpool spot price scrape IoT project for CMP408

##### 1. Guidelines
> Your task is to undertake a small project related to IoT and Cloud Secure Development to demonstrate the application of the skills learned in this module in a way that interests you and to explore the area in general.
> ##### <ins>IoT, Software and Cloud components:</ins>
> *These three components are implementation based. Students must demonstrate combinations of ideas developed over the module lectures and labs.*
> - The IoT component can be presented with the actual physical device (RPi or any similar platform).
> - The Software part should demonstrate software design, architecture, and best development practices. Students can use sf.net or similar sources for this component; however, the project report should clearly indicate your contribution and changes.
> - The Cloud component should integrate various services to form a cohesive system.

##### 2. My Implementation
A tool that gets Nordpool hourly electricity tariff data for the current and next day daily or when triggered with a button press. The tariff values are colour-coded based on how expensive they are (i.e., red is expensive, green is affordable, etc.). An LED light is changed every hour to a colour that corresponds with the colour-coded tariff value for that time. The coloured 2 day data is also sent to a simple site hosted on an AWS EC2 instance and displayed.
