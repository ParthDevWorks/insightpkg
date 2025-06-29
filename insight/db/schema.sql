CREATE TABLE if not exists pypi_packages (
    package_name TEXT NOT NULL,
    package_version TEXT NOT NULL,
    package_upload_date DATE NOT NULL,
    package_upload_time TIME WITH TIME ZONE NOT NULL,
    package_github_link TEXT,
    package_description TEXT,
    PRIMARY KEY (package_name, package_version)
);

CREATE TABLE if not exists github_info (
    github_link TEXT NOT NULL,
    stars INT NOT NULL,
    watchers INT NOT NULL,
    forks INT NOT NULL,
    open_issues INT NOT NULL,
    created_date DATE NOT NULL,
    last_updated_date DATE NOT NULL,
    license TEXT,
    PRIMARY KEY (github_link)
);

CREATE TABLE if not exists release_notes_info (
    github_link TEXT NOT NULL,
    release_tag TEXT,
    published_date DATE NOT NULL,
    release_notes TEXT,
    PRIMARY KEY (github_link, release_tag)
    FOREIGN KEY (github_link) REFERENCES github_info(github_link)
);