# multiclass-perceptron

N.B Occorre avere numpy e matplotlib installati.   

Gli script creati sono:   

"VotedPerceptron.py" per il classificatore binario.   
Si possono testare le funzioni booleane passando come parametro allo script in
fase di esecuzione   

python VotedPerceptron.py OR   
python VotedPerceptron.py NOR   
python VotedPerceptron.py AND   
python VotedPerceptron.py NAND   
python VotedPerceptron.py XOR   

Se non si passa alcun parametro verrà generato un dataset linearmente separabile
con due feature.   

-------------------------------------------------------------------------

Percetron Multiclasse   
N.B sono stati testati con i dataset di train e test USPS (riconoscimento
caratteri manoscritti)   
non occorre passare alcun parametro, basta che il file di train e test siano
nella cartella dove vengono eseguiti gli script, con il nome di zip.train e
zip.test   

"Perceptron_allpairs.py"   
"Perceptron_ovr.py"   
