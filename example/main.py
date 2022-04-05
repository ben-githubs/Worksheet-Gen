import logging
from pathlib import Path

from wsgen import Worksheet
import problems as prob

p = prob.ArrangingLetters('Arranging Letters', Path('templates/probems/arranging_letters.tex'))

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logging.debug('Logger set up complete.')

def main():

    worksheet = Worksheet()
    worksheet.append(prob.ArrangingLetters('Arranging Letters', Path('templates/problems/arranging_letters.tex')))
    worksheet.append(prob.BinomialExpansionSolveN('Binomial', Path('templates/problems/binomial_expansion_solve_for_n.tex')))
    worksheet.save_to_file(Path('worksheet.tex'), overwrite=True)

if __name__ == '__main__':
    main()
