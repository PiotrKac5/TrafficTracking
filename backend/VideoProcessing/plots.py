from flask import Flask, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
CORS(app)

@app.route('/plots')
def plot():
    # Generate a plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4, 5], [10, 20, 25, 30, 32])
    ax.set(xlabel='x-axis', ylabel='y-axis', title='Sample Plot')

    # Save plot to a bytes buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the figure to free memory

    # Send the image to the client
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
