#include <poppler-document.h>
#include <poppler-page.h>
#include <iostream>
#include <fstream>
#include <memory>
#include <nlohmann/json.hpp>
#include <regex>
#include <map>
#include <sstream>

using json = nlohmann::json;

bool is_probable_heading(const std::string& line, const std::vector<std::string>& keywords) {
    for (const auto& keyword : keywords) {
        std::regex pattern("(\\b|\\s|^)" + keyword + "(\\b|\\s|$)", std::regex::icase);

        if (std::regex_search(line, pattern)) {
            return true;
        }
    }
    return false;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: pdf_ingest <path-to-pdf>\n";
        return 1;
    }

    std::unique_ptr<poppler::document> doc(poppler::document::load_from_file(argv[1]));
    if (!doc) {
        std::cerr << "Failed to open PDF.\n";
        return 1;
    }

    std::ofstream txt_out("output.txt");
    json structured_output;

    std::string full_text;

    for (int i = 0; i < doc->pages(); ++i) {
        std::unique_ptr<poppler::page> page(doc->create_page(i));
        if (page) {
            std::vector<char> raw = page->text().to_utf8();
            std::string text(raw.begin(), raw.end());

            txt_out << "Page " << (i + 1) << ":\n" << text << "\n\n";
            structured_output["page_" + std::to_string(i + 1)] = text;

            full_text += "\n" + text;
        }
    }
    txt_out.close();

    std::vector<std::string> keywords = {
        "abstract", "introduction", "preliminaries", "background", "related work",
        "method", "approach", "proof", "model", "experiments", "evaluation", "results",
        "discussion", "conclusion", "references", "acknowledgments", "appendix"
    };

    std::istringstream iss(full_text);
    std::string line;
    std::string current_heading = "preamble";
    std::map<std::string, std::string> sections;

    while (std::getline(iss, line)) {
        std::string trimmed = std::regex_replace(line, std::regex(R"(^\s+|\s+$)"), "");

        if (is_probable_heading(trimmed, keywords)) {
            current_heading = trimmed;
            if (sections.find(current_heading) == sections.end()) {
                sections[current_heading] = "";
            }
        } else {
            sections[current_heading] += line + "\n";
        }
    }

    structured_output["sections"] = json::object();
    for (const auto& [section, content] : sections) {
        structured_output["sections"][section] = content;
    }

    std::ofstream json_out("output.json");
    json_out << structured_output.dump(2);
    json_out.close();

    std::cout << "Extraction complete. Files saved: output.txt and output.json\n";
    return 0;
}
