if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--unique_id")
    args = parser.parse_args()

    names_to_check = pd.read_csv(args.filename)
    names.firstname = names.firstname.apply(lambda x: str(x).title())
    names.lastname = names.lastname.apply(lambda x: str(x).title())
    names_to_check["full_name"] = (
        names_to_check.firstname + " " + names_to_check.lastname
    )

    # Run names through wikipedia API
    wiki_dict = run_wikipedia_api(names_to_check)

    # Applies wikpedia results to original dataframe
    names_to_check["wiki_name"] = names_to_check.email.apply(
        lambda x: get_wiki_info(x, "name", wiki_dict)
    )
    names_to_check["wiki_bio"] = names_to_check.email.apply(
        lambda x: get_wiki_info(x, "bio", wiki_dict)
    )

    # Filters down to names that have wikipedia matches
    names_to_check = names_to_check[names_to_check.wiki_bio != ""].copy()
    wiki_matched = find_matches(name_to_check)
