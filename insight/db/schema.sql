CREATE TABLE if not exists pypi_packages (
    package_name TEXT NOT NULL,
    package_version TEXT NOT NULL,
    package_date DATE NOT NULL,
    package_github_link TEXT,
    package_description TEXT,
    PRIMARY KEY (package_name, package_version)
);