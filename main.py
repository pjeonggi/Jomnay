from src.fileExporter import FileExporter

def main():
	file_path = "data/myExpenses1.csv"

	exporter = FileExporter(file_path)
	exporter.check_file()
	exporter.read_file()
	exporter.check_columns()
	exporter.clean_data()
	exporter.export_all()
	exporter.item_summary()
	exporter.monthly_summary()
	exporter.category_summary()
	exporter.amount_summary()


if __name__ == "__main__":
	main()