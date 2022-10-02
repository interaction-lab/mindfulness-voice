import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

gender_codings = {'Male': 0, 'Female': 1, 'Child': 2}
accent_codings = {'American': 0, 'British': 1, 'Australian': 2}


def parse_row(row):
    return [gender_codings[row[0]], accent_codings[row[1]], int(row[2]), int(row[3]), int(row[4])]


def load_settings_from_file(filename, loaded):
    init_size = len(loaded)
    with open(filename, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            loaded.append(parse_row(row))
    return len(loaded) - init_size


data_to_fit = []
audio_size = load_settings_from_file('audio_settings.csv', data_to_fit)
alexa_size = load_settings_from_file('alexa_settings.csv', data_to_fit)
blossom_size = load_settings_from_file('blossom_settings.csv', data_to_fit)
print([audio_size, alexa_size, blossom_size])

pca_model = PCA(n_components=2)
fitted_data = pca_model.fit_transform(data_to_fit)

plt.scatter([x[0] for x in (fitted_data[0:audio_size])], [x[1] for x in (fitted_data[0:audio_size])], c='r')
plt.scatter([x[0] for x in (fitted_data[audio_size:audio_size+alexa_size])], [x[1] for x in (fitted_data[audio_size:audio_size+alexa_size])], c='g')
plt.scatter([x[0] for x in (fitted_data[audio_size+alexa_size:audio_size+alexa_size+blossom_size])], [x[1] for x in (fitted_data[audio_size+alexa_size:audio_size+alexa_size+blossom_size])], c='b')
plt.show()
