import metrics.schools as schools

if __name__ == '__main__':
    data = schools.load_schools()
    schools.save_schools_data(data)