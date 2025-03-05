import csv

LOG_FILE = "server_usage_log.csv"  # Input CSV file
WIDTH = 50  # Width of the ASCII plot
MAX_VALUE = 100  # Assuming CPU and memory percentage are in the 0-100 range

def load_data():
    """Read the last records from the CSV log file."""
    records = []
    try:
        with open(LOG_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            records = [row for row in reader][-50:]  # Take last 50 entries
    except FileNotFoundError:
        print("No log file found.")
    return records

def create_plot(records):
    """Generate ASCII plot for CPU and memory usage with axis labels and legend."""
    plot_lines = []

    # Add legend
    plot_lines.append("Legend: x = CPU usage, o = Memory usage")
    plot_lines.append("Time               | Usage Plot")
    plot_lines.append("-" * (WIDTH + 20))

    for timestamp, cpu, memory in records:
        try:
            cpu = float(cpu)
            memory = float(memory)

            # Map values to the plot width, ensuring 100% is inside the plot range
            cpu_pos = min(int((cpu / MAX_VALUE) * WIDTH), WIDTH - 1)
            mem_pos = min(int((memory / MAX_VALUE) * WIDTH), WIDTH - 1)

            # Create empty line
            line = [" "] * WIDTH
            line[cpu_pos] = "x"  # CPU usage
            line[mem_pos] = "o"  # Memory usage

            plot_lines.append(f"{timestamp[:16]} | " + "".join(line))
        except ValueError:
            continue  # Skip invalid lines

    # Add axis labels
    axis_labels = "0%" + " " * (WIDTH // 2 - 2) + "50%" + " " * (WIDTH // 2 - 3) + "100%"
    axis_line = " " * 18 + "|" + "-" * WIDTH
    plot_lines.append("\n" + axis_line)
    plot_lines.append(" " * 18 + "|" + axis_labels + "\n")  # Ensure newline at the end

    return "\n".join(plot_lines) + "\n"  # Ensure final newline

def main():
    records = load_data()
    if records:
        plot_output = create_plot(records)
        print(plot_output)  # Print directly to terminal

if __name__ == "__main__":
    main()