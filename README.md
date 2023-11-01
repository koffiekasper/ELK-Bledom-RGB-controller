# ELK-Bledom-RGB-controller
Python files to control ELK-Bledom RGB strip.
This project includes a simple Flask API, meant for user control. Also it includes a RGB Strip controller, consting of a Service and Repository in which logic is placed.

### Starting up
1. Create a file called ".env" in the main folder.
2. Fill it with the following contents, replacing ADDRESS and SERVICE with the values of your RGB controller
`ADDRESS=EEBA4CF3-B124-5AFE-3FCF-D0EBD7206E53`   
`GATTHANDLE=13`
3. Install PIP dependencies
4. Run api,py with Python
5. Run run_controller.py with Python

### API Calls
`/set_speed/(VAL)`
- Sets the rate per second in which iterating color effects are updated
  
`/mode/random`
- Enabled the random effect
  
`/toggle`
- Toggles the light on or off

`/color/(Color name)`
- Takes as input a color string in the English language. If the color is recognized it sets the color.


`/hexcolor/(hex code)`
- Takes as input a hex RGB color code and sets the color accordingly

`/setiteratelist` (post)
- Takes in the `colors` argument in the POST body as a list of colors in English separated by commas. It then sets the animation list to these colors
 
`/setiteratelist/rainbow` 
- Sets the color iteration list to the rainbow