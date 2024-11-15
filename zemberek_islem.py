import jpype
import jpype.imports
import pandas as pd
from jpype.types import *

zemberek_jar_path = "C:\\Users\\hilal\\Zemberek-Python-Examples\\zemberek-full.jar"

if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[zemberek_jar_path])

TurkishMorphology = jpype.JClass("zemberek.morphology.TurkishMorphology")
morphology = TurkishMorphology.createWithDefaults()

file_path = 'cleaned_zaman.csv'
data = pd.read_csv(file_path)

simplified_output = []

for index, row in data.iterrows():
    poem_line = row['poem_cleaned']
    if pd.notnull(poem_line):
        analysis = morphology.analyzeSentence(poem_line)
        processed_line = []
        
        for result in analysis:
            for single_analysis in result.getAnalysisResults():
                root = single_analysis.getDictionaryItem().lemma
                pos = single_analysis.getDictionaryItem().primaryPos.name()
                processed_line.append({"input": result.getInput(), "root": root, "type": pos})
        
        simplified_output.append({"original_line": poem_line, "processed": processed_line})

output_df = pd.DataFrame(simplified_output)
output_df.to_csv('simplified_zaman.csv', index=False, encoding='utf-8-sig')

jpype.shutdownJVM()
