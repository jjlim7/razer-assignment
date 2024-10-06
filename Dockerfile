# Step 1: Use an official Python runtime as a parent image
FROM python:3.12-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Step 4: Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the current directory contents into the container at /app
COPY . /app/

# Step 6: Set environment variables for Flask
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Step 7: Expose port 5000 to allow outside access
EXPOSE 5000

# Step 8: Run the Flask app (or use Gunicorn for production)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
