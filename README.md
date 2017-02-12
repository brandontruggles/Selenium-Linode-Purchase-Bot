# Selenium Linode Bot
This is a simple Python bot which uses Selenium to navigate the website [http://www.linode.com/](http://www.linode.com/)  and purchase servers. Users can configure how many servers they want to order, as well as the credentials associated with their Linode account by editing the included checkout.conf JSON file. The script is configured to use Chromedriver, which is included as a Pip dependency, but PhantomJS is included as a NodeJS dependency in the case that you want to use a headless webdriver.

## Installation Instructions (Linux/Mac)

1. Make sure that you have Python 2.7.X installed, along with Pip.

2. Install Node.JS and NPM.

3. Download or clone this repository to a directory on your machine.

4. Add the directory containing this project into your global PYTHONPATH environment variable. *NOTE: If you get an error stating that checkout.conf cannot be found, or that it contains invalid JSON, you may not have performed this step.*

5. Open the terminal, navigate to the project directory, and type the command `pip install -r requirements.txt`. This should install the Python dependencies Selenium and Chromedriver. *NOTE: On Mac, the dependency chromedriver-installer may not download. If this is the case, you will have to install Chromedriver manually.*

6. From the terminal, type the command `npm install`. This should install PhantomJS.

7. Edit the checkout.conf JSON file to your liking, but make sure that it still contains valid JSON syntax.

8. You may edit autocheckout.py to use PhantomJS instead of Chromedriver if you do not wish to view the browser navigation performed by the script. 

9. Run the program from the terminal with `python autocheckout.py`.

## Installation Instructions (Windows)

This script has not been tested for Windows, but it should still work if a similar procedure is followed as the one for Linux/Mac.
