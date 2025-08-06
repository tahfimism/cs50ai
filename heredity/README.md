# Heredity Probability AI

This project is an implementation of a Bayesian network to infer the probability of a person having a certain number of genes and exhibiting a related trait based on their family history. This was completed as part of Harvard's CS50 Introduction to Artificial Intelligence course.

## Project Overview

The program takes a dataset of a family as a CSV file. This file defines each person, their parents (if known), and whether they are known to exhibit a specific genetic trait. The AI then calculates, for each person, two key probability distributions:

1.  **Gene Distribution:** The probability that the person has 0, 1, or 2 copies of the gene in question.
2.  **Trait Distribution:** The probability that the person does or does not exhibit the trait.

This is a classic problem of reasoning under uncertainty, where we use observable evidence (family relationships and known traits) to infer the probabilities of hidden states (the specific genetic makeup of individuals).

## How It Works: The Algorithm

The core of the AI is built on the principles of Bayesian inference. The program considers every possible "state of the world"—a specific scenario where every person has a defined number of genes and a defined trait status.

1.  **Generate All Possibilities:** The program first generates a powerset of all possible scenarios. It iterates through every combination of people who could have the trait, and for each of those, it iterates through every combination of how many genes each person could have.

2.  **Calculate Joint Probability:** For each single, specific scenario, the `joint_probability` function is called to calculate the probability of that exact state of the world occurring. This is done by multiplying the individual probabilities of each person's genetic and trait status, conditioned on their parents' genes.

3.  **Aggregate Probabilities:** The `update` function takes the joint probability of a single scenario and adds it to a running total for each person. For example, if a scenario where "Harry has 1 gene" has a probability of 0.005, that value is added to the total for "Harry's probability of having 1 gene." This process is repeated for all valid scenarios.

4.  **Normalize Results:** After checking all scenarios, the `normalize` function is called. It takes the aggregated totals for each distribution (e.g., Harry's gene probabilities for 0, 1, and 2 copies) and scales them so that they sum to 1, converting them into a proper probability distribution.

## Implemented Functions

The core logic of the AI was implemented in the following three functions:

### `joint_probability(people, one_gene, two_genes, have_trait)`

This function computes the probability of a single, complete assignment of genes and traits for everyone in the family.

-   **Inputs:**
    -   `people`: The dictionary containing all family members and their parent relationships.
    -   `one_gene`: A set of names of people who have one copy of the gene in this scenario.
    -   `two_genes`: A set of names of people who have two copies of the gene.
    -   `have_trait`: A set of names of people who exhibit the trait in this scenario.
-   **Logic:**
    1.  It iterates through each person in the family.
    2.  For each person, it calculates `P(person has X genes AND has Y trait)`. This is broken down into `P(genes) * P(trait | genes)`.
    3.  **Gene Probability `P(genes)`:**
        -   If a person has no parents listed, their gene probability is taken directly from the unconditional `PROBS["gene"]` distribution.
        -   If a person has parents, their gene probability is conditional on the parents' genes. It calculates the probability of inheriting the gene from each parent (factoring in `PROBS["mutation"]`) and combines them to find the probability of the child having 0, 1, or 2 genes.
    4.  **Trait Probability `P(trait | genes)`:** This is a direct lookup from `PROBS["trait"]` based on the person's gene count for this scenario.
    5.  The final joint probability is the product of these individual probabilities calculated for every person in the family.

### `update(probabilities, one_gene, two_genes, have_trait, p)`

This function acts as an accumulator. After `joint_probability` calculates the probability `p` of a single world state, this function adds that probability to the appropriate running totals.

-   **Logic:**
    1.  It iterates through each person.
    2.  It determines their gene count (0, 1, or 2) and trait status (True or False) for the given scenario based on the `one_gene`, `two_genes`, and `have_trait` sets.
    3.  It adds the probability `p` to the corresponding entries in the main `probabilities` dictionary. For example, if Harry had 1 gene and the trait, `p` would be added to `probabilities["Harry"]["gene"][1]` and `probabilities["Harry"]["trait"][True]`.

### `normalize(probabilities)`

This is the final step. This function converts the aggregated scores in the `probabilities` dictionary into true probability distributions that sum to 1.

-   **Logic:**
    1.  It iterates through each person and each of their distributions (`gene` and `trait`).
    2.  For each distribution, it calculates the sum of all values (e.g., `sum = prob_gene_0 + prob_gene_1 + prob_gene_2`).
    3.  It then divides each value in the distribution by that sum. This ensures the new values maintain their relative proportions while summing to 1.

## Real-World Applications

This specific algorithm has direct and significant applications in the real world, primarily in fields that rely on understanding inheritance patterns without complete genetic data:

-   **Genetic Counseling:** This is the canonical use case. Counselors use this exact type of modeling to advise prospective parents. By constructing a family pedigree and noting known instances of a genetic disorder (like Cystic Fibrosis or Tay-Sachs disease), they can calculate the probability of a child inheriting the condition. This provides families with crucial, data-driven information for making life decisions.

-   **Agriculture and Livestock Breeding:** This model is used to predict the inheritance of desirable traits in plants and animals. Breeders maintain extensive pedigree records and track traits like milk production, muscle mass, crop yield, or disease resistance. By applying this algorithm, they can estimate the probability of offspring inheriting valuable genes from a particular pairing, optimizing their breeding programs without needing to conduct expensive genetic sequencing on every individual.

## How to Run the Program

1.  Ensure you have Python 3 installed.
2.  Clone the repository.
3.  Run the program from the command line, passing the path to a data file as an argument. Sample data files are included in the `data/` directory.

```bash
python heredity.py data/family0.csv
```

The output will be printed to the console or terminal, showing the final calculated probability distributions for each person in the dataset.
