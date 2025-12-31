# laptop-price-predictor
this is a project that I have done for improving my python skills

## Laptop Price Predictor
A desktop application that predicts laptop prices using machine learning. Built with Python, PyQt5, and scikit-learn, this tool uses historical laptop data to estimate prices based on hardware specifications.

Features
- Price Prediction: Estimates laptop prices using a Decision Tree Classifier

- Automated Data Collection: Fetches real laptop data from Zoomit.ir (Iranian tech marketplace)

- User-Friendly Interface: Persian-language GUI with intuitive input fields

- Data Validation: Comprehensive input checking and error handling

- Local Database: SQLite storage for collected laptop specifications

- Real-time Prediction: Instant price estimates based on user inputs


## How It Works

### Data Collection
On first run, the application:

Connects to Zoomit.ir API (Iranian tech marketplace)
Scrapes laptop specifications and prices from 63 pages of products
Stores the data in a local SQLite database (database.db)
Subsequent runs use the cached data without API calls

### Machine Learning Model
- Uses a Decision Tree Classifier from scikit-learn
- Encodes categorical data (CPU, GPU, disk type) using LabelEncoder
- Trains on 6 features: CPU, GPU, RAM, disk size, disk type, and screen size
- Predicts price as the target variable

### Input Features
CPU: Processor model (e.g., "Intel Core i7", "Apple M1 Pro")<br>
GPU: Graphics card (e.g., "Nvidia RTX 4060", "onboard")<br>
RAM: Memory size in GB (e.g., 8, 16, 32)<br>
Disk Size: Storage in GB (e.g., 256, 512, 1024)<br>
Disk Type: Storage technology (e.g., "SSD", "HDD", "NVMe SSD")<br>
Display Size: Screen size in inches (e.g., 13.3, 15.6, 17.3)<br>

### Limitations
data is trained on Iranian market data (Zoomit.ir) so all the prices predictions in Iranian Tomans (IRR). Also there is a problem, prices accuracy(being up to date) also depend on the last time that data have been scraped. If you want to make sure that all the datas are up to date, you can simply remove the database file which is 'database.db' which triggers the program to scrape the web again and store the new data.  
