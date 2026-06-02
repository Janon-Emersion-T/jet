import datetime
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from core.vector_memory.vector_store import add_vector_memory


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"
CATEGORY_FILE = DATA_DIR / "programming_knowledge_catalog.json"
SENIOR_LANGUAGE_FILE = DATA_DIR / "senior_engineer_language_catalog.json"
AUTONOMOUS_TOPICS_FILE = DATA_DIR / "autonomous_learning_topics.json"
MANIFEST_DIR = DATA_DIR / "programming_knowledge_manifests"
LOG_FILE = STORAGE_DIR / "programming_learning_log.jsonl"

DEFAULT_HEADERS = {
    "User-Agent": "JARVIS-Programming-Knowledge-Engine/1.0 (+local private assistant)"
}

UPDATE_PREFIXES = [
    "learn ",
    "teach yourself ",
    "master ",
    "build ",
    "update ",
    "refresh ",
    "relearn ",
    "study ",
]

FORCE_PREFIXES = [
    "force update ",
    "force relearn ",
]

STATUS_PREFIXES = [
    "check ",
    "show ",
]

TOPIC_STOPWORDS = {
    "knowledge",
    "properly",
    "latest",
    "official",
    "sources",
    "from",
    "the",
    "and",
    "language",
    "languages",
    "programming",
}

ALL_TOPICS_ALIASES = {
    "all programming languages",
    "all languages",
    "all programming frameworks",
    "all frameworks",
    "all programming languages and frameworks",
    "all learning topics",
    "all topics",
    "all 200 topics",
    "everything in the curriculum",
    "everything",
    "all",
}

CURRICULUM_TRACK_PRIORITY = {
    "software-development": 0,
    "seo": 1,
    "digital-marketing": 2,
    "computer-hardware": 3,
    "rest-of-world": 4,
}

SOFTWARE_DEVELOPMENT_KEYWORDS = (
    "software",
    "architecture",
    "frontend",
    "backend",
    "api",
    "testing",
    "devops",
    "deployment",
    "security",
    "database",
    "version control",
    "programming",
    "framework",
    "runtime",
    "react",
    "node",
    "php",
    "laravel",
    "python",
    "javascript",
    "typescript",
    "css",
    "html",
    "system design",
    "distributed systems",
    "performance optimization",
    "refactoring",
    "clean code",
)

SEO_KEYWORDS = (
    "seo",
    "search engine",
    "crawl",
    "indexing",
    "structured data",
    "schema",
    "canonical",
    "robots",
    "sitemap",
    "serp",
    "technical seo",
)

DIGITAL_MARKETING_KEYWORDS = (
    "marketing",
    "campaign",
    "conversion",
    "brand",
    "growth",
    "analytics",
    "ads",
    "advertising",
    "attribution",
    "social media",
    "email marketing",
    "lead generation",
)

COMPUTER_HARDWARE_KEYWORDS = (
    "hardware",
    "electronics",
    "embedded",
    "iot",
    "robotics",
    "microcontroller",
    "firmware",
    "cpu",
    "gpu",
    "memory hierarchy",
    "circuits",
)

SOURCE_GROUPS = {
    "computer-foundations": [
        {"name": "Nand2Tetris", "url": "https://www.nand2tetris.org/", "type": "foundational-course", "priority": 9},
        {"name": "CS50 Computer Science Courses", "url": "https://cs50.harvard.edu/x/", "type": "foundational-course", "priority": 8},
    ],
    "math-logic-learning": [
        {"name": "Khan Academy Computing", "url": "https://www.khanacademy.org/computing", "type": "practical-course", "priority": 8},
        {"name": "MIT OpenCourseWare Electrical Engineering and Computer Science", "url": "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/", "type": "university-course", "priority": 8},
    ],
    "english-communication": [
        {"name": "British Council Learn English", "url": "https://learnenglish.britishcouncil.org/", "type": "official-learning-platform", "priority": 8},
        {"name": "Cambridge English Learning Resources", "url": "https://www.cambridgeenglish.org/learning-english/", "type": "official-learning-platform", "priority": 8},
    ],
    "internet-web": [
        {"name": "MDN Learn Web Development", "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development", "type": "developer-reference", "priority": 9},
        {"name": "Cloudflare Learning Center", "url": "https://www.cloudflare.com/learning/", "type": "practical-guide", "priority": 8},
    ],
    "software-engineering": [
        {"name": "Google Engineering Practices Documentation", "url": "https://google.github.io/eng-practices/", "type": "engineering-guide", "priority": 9},
        {"name": "Atlassian Software Development Guides", "url": "https://www.atlassian.com/software", "type": "practical-guide", "priority": 7},
        {"name": "Martin Fowler", "url": "https://martinfowler.com/", "type": "architecture-guide", "priority": 8},
    ],
    "git-collaboration": [
        {"name": "Git Documentation", "url": "https://git-scm.com/docs", "type": "official-documentation", "priority": 10},
        {"name": "GitHub Docs", "url": "https://docs.github.com/en", "type": "official-documentation", "priority": 10},
    ],
    "architecture-systems": [
        {"name": "AWS Architecture Center", "url": "https://aws.amazon.com/architecture/", "type": "cloud-architecture", "priority": 9},
        {"name": "Google Cloud Architecture Center", "url": "https://cloud.google.com/architecture", "type": "cloud-architecture", "priority": 9},
        {"name": "Martin Fowler Architecture", "url": "https://martinfowler.com/architecture/", "type": "architecture-guide", "priority": 8},
    ],
    "databases-data": [
        {"name": "PostgreSQL Documentation", "url": "https://www.postgresql.org/docs/", "type": "official-documentation", "priority": 9},
        {"name": "MongoDB Documentation", "url": "https://www.mongodb.com/docs/", "type": "official-documentation", "priority": 8},
        {"name": "Microsoft SQL Documentation", "url": "https://learn.microsoft.com/en-us/sql/", "type": "official-documentation", "priority": 8},
    ],
    "security-fundamentals": [
        {"name": "OWASP Developer Guide", "url": "https://devguide.owasp.org/", "type": "security-guide", "priority": 10},
        {"name": "OWASP Top 10", "url": "https://owasp.org/www-project-top-ten/", "type": "security-standard", "priority": 10},
        {"name": "Cloudflare Security Learning", "url": "https://www.cloudflare.com/learning/security/", "type": "practical-guide", "priority": 8},
    ],
    "devops-cloud": [
        {"name": "Docker Docs", "url": "https://docs.docker.com/", "type": "official-documentation", "priority": 10},
        {"name": "Kubernetes Documentation", "url": "https://kubernetes.io/docs/", "type": "official-documentation", "priority": 10},
        {"name": "Terraform Documentation", "url": "https://developer.hashicorp.com/terraform/docs", "type": "official-documentation", "priority": 9},
        {"name": "GitHub Actions Documentation", "url": "https://docs.github.com/en/actions", "type": "official-documentation", "priority": 9},
    ],
    "operating-systems": [
        {"name": "Microsoft Learn Windows", "url": "https://learn.microsoft.com/en-us/windows/", "type": "official-documentation", "priority": 8},
        {"name": "Linux Foundation Training", "url": "https://training.linuxfoundation.org/", "type": "official-learning-platform", "priority": 8},
        {"name": "Apple Developer Documentation", "url": "https://developer.apple.com/documentation/", "type": "official-documentation", "priority": 8},
    ],
    "frontend-ux": [
        {"name": "MDN Learn Web Development", "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development", "type": "developer-reference", "priority": 9},
        {"name": "W3C Accessibility Guidelines", "url": "https://www.w3.org/WAI/standards-guidelines/wcag/", "type": "official-standard", "priority": 10},
        {"name": "web.dev", "url": "https://web.dev/", "type": "practical-guide", "priority": 8},
    ],
    "backend-api": [
        {"name": "MDN Web APIs", "url": "https://developer.mozilla.org/en-US/docs/Web/API", "type": "developer-reference", "priority": 8},
        {"name": "OpenAPI Specification", "url": "https://spec.openapis.org/oas/latest.html", "type": "official-standard", "priority": 9},
        {"name": "GraphQL Learn", "url": "https://graphql.org/learn/", "type": "official-documentation", "priority": 9},
    ],
    "ai-ml": [
        {"name": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "type": "official-course", "priority": 9},
        {"name": "PyTorch Tutorials", "url": "https://pytorch.org/tutorials/", "type": "official-documentation", "priority": 8},
        {"name": "Hugging Face Learn", "url": "https://huggingface.co/learn", "type": "official-learning-platform", "priority": 8},
    ],
    "mobile-platforms": [
        {"name": "Android Developers", "url": "https://developer.android.com/", "type": "official-documentation", "priority": 10},
        {"name": "Apple Developer Documentation", "url": "https://developer.apple.com/documentation/", "type": "official-documentation", "priority": 10},
        {"name": "Flutter Docs", "url": "https://docs.flutter.dev/", "type": "official-documentation", "priority": 8},
    ],
    "business-product": [
        {"name": "Atlassian Agile Coach", "url": "https://www.atlassian.com/agile", "type": "practical-guide", "priority": 8},
        {"name": "Google for Startups", "url": "https://startup.google.com/", "type": "practical-guide", "priority": 7},
        {"name": "Stripe Guides", "url": "https://stripe.com/resources", "type": "business-guide", "priority": 7},
    ],
    "compliance": [
        {"name": "GDPR.eu", "url": "https://gdpr.eu/", "type": "compliance-guide", "priority": 8},
        {"name": "PCI Security Standards Council", "url": "https://www.pcisecuritystandards.org/", "type": "official-standard", "priority": 9},
        {"name": "HHS HIPAA Guidance", "url": "https://www.hhs.gov/hipaa/index.html", "type": "official-guidance", "priority": 8},
    ],
    "cybersecurity-advanced": [
        {"name": "NIST Cybersecurity Resources", "url": "https://www.nist.gov/cybersecurity", "type": "official-guidance", "priority": 10},
        {"name": "OWASP Projects", "url": "https://owasp.org/projects/", "type": "security-guide", "priority": 9},
        {"name": "MITRE ATT&CK", "url": "https://attack.mitre.org/", "type": "security-framework", "priority": 9},
    ],
    "hardware-electronics": [
        {"name": "Arduino Documentation", "url": "https://docs.arduino.cc/", "type": "official-documentation", "priority": 8},
        {"name": "Raspberry Pi Documentation", "url": "https://www.raspberrypi.com/documentation/", "type": "official-documentation", "priority": 8},
        {"name": "All About Circuits", "url": "https://www.allaboutcircuits.com/textbook/", "type": "reference", "priority": 7},
    ],
    "lang-c-family": [
        {"name": "cppreference C Language", "url": "https://en.cppreference.com/w/c/language", "type": "language-reference", "priority": 9},
        {"name": "GCC Manuals", "url": "https://gcc.gnu.org/onlinedocs/", "type": "compiler-reference", "priority": 8},
    ],
    "lang-cpp": [
        {"name": "cppreference C++ Language", "url": "https://en.cppreference.com/w/cpp/language", "type": "language-reference", "priority": 10},
        {"name": "ISO C++ Core Guidelines", "url": "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines", "type": "best-practices", "priority": 9},
    ],
    "lang-csharp-dotnet": [
        {"name": "C# Documentation", "url": "https://learn.microsoft.com/en-us/dotnet/csharp/", "type": "official-documentation", "priority": 10},
        {"name": ".NET Documentation", "url": "https://learn.microsoft.com/en-us/dotnet/", "type": "platform-reference", "priority": 9},
    ],
    "lang-java-jvm": [
        {"name": "dev.java Learn", "url": "https://dev.java/learn/", "type": "official-learning-path", "priority": 9},
        {"name": "Oracle Java Documentation", "url": "https://docs.oracle.com/en/java/", "type": "official-documentation", "priority": 9},
        {"name": "JVM Specification", "url": "https://docs.oracle.com/javase/specs/", "type": "platform-specification", "priority": 8},
    ],
    "lang-python": [
        {"name": "Python Documentation", "url": "https://docs.python.org/3/", "type": "official-documentation", "priority": 10},
        {"name": "Python Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "official-tutorial", "priority": 9},
        {"name": "Python Library Reference", "url": "https://docs.python.org/3/library/", "type": "standard-library-reference", "priority": 9},
    ],
    "lang-javascript-typescript": [
        {"name": "ECMAScript Specification", "url": "https://tc39.es/ecma262/", "type": "official-standard", "priority": 10},
        {"name": "MDN JavaScript Reference", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference", "type": "developer-reference", "priority": 9},
        {"name": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/", "type": "official-documentation", "priority": 9},
    ],
    "lang-php-web": [
        {"name": "PHP Manual", "url": "https://www.php.net/manual/en/", "type": "official-documentation", "priority": 10},
        {"name": "PHP Language Reference", "url": "https://www.php.net/manual/en/langref.php", "type": "language-reference", "priority": 9},
    ],
    "lang-ruby": [
        {"name": "Ruby Documentation", "url": "https://www.ruby-lang.org/en/documentation/", "type": "official-documentation", "priority": 9},
        {"name": "Ruby Core API", "url": "https://ruby-doc.org/core/", "type": "api-reference", "priority": 8},
    ],
    "lang-go": [
        {"name": "Go Documentation", "url": "https://go.dev/doc/", "type": "official-documentation", "priority": 10},
        {"name": "Go Language Specification", "url": "https://go.dev/ref/spec", "type": "language-specification", "priority": 9},
    ],
    "lang-rust": [
        {"name": "Rust Documentation", "url": "https://doc.rust-lang.org/", "type": "official-documentation", "priority": 10},
        {"name": "The Rust Programming Language", "url": "https://doc.rust-lang.org/book/", "type": "official-book", "priority": 10},
        {"name": "Rust Standard Library", "url": "https://doc.rust-lang.org/std/", "type": "standard-library-reference", "priority": 9},
    ],
    "lang-swift-objc": [
        {"name": "Swift Documentation", "url": "https://www.swift.org/documentation/", "type": "official-documentation", "priority": 10},
        {"name": "Apple Developer Documentation", "url": "https://developer.apple.com/documentation/", "type": "platform-reference", "priority": 10},
    ],
    "lang-kotlin": [
        {"name": "Kotlin Documentation", "url": "https://kotlinlang.org/docs/home.html", "type": "official-documentation", "priority": 10},
        {"name": "Kotlin Language Reference", "url": "https://kotlinlang.org/docs/reference/", "type": "language-reference", "priority": 9},
    ],
    "lang-dart": [
        {"name": "Dart Documentation", "url": "https://dart.dev/guides", "type": "official-documentation", "priority": 9},
        {"name": "Flutter Documentation", "url": "https://docs.flutter.dev/", "type": "platform-reference", "priority": 9},
    ],
    "lang-scala": [
        {"name": "Scala Documentation", "url": "https://docs.scala-lang.org/", "type": "official-documentation", "priority": 9},
        {"name": "Scala 3 Reference", "url": "https://docs.scala-lang.org/scala3/reference/", "type": "language-reference", "priority": 8},
    ],
    "lang-perl": [
        {"name": "Perl Documentation", "url": "https://perldoc.perl.org/", "type": "official-documentation", "priority": 9},
    ],
    "lang-lua": [
        {"name": "Lua Reference Manual", "url": "https://www.lua.org/manual/", "type": "official-documentation", "priority": 9},
    ],
    "lang-r": [
        {"name": "R Manuals", "url": "https://cran.r-project.org/manuals.html", "type": "official-documentation", "priority": 9},
    ],
    "lang-julia": [
        {"name": "Julia Documentation", "url": "https://docs.julialang.org/", "type": "official-documentation", "priority": 9},
    ],
    "lang-functional": [
        {"name": "Haskell Documentation", "url": "https://www.haskell.org/documentation/", "type": "official-documentation", "priority": 9},
        {"name": "Elixir Documentation", "url": "https://hexdocs.pm/elixir/introduction.html", "type": "official-documentation", "priority": 9},
        {"name": "Erlang Documentation", "url": "https://www.erlang.org/docs", "type": "official-documentation", "priority": 9},
        {"name": "F# Documentation", "url": "https://learn.microsoft.com/en-us/dotnet/fsharp/", "type": "official-documentation", "priority": 9},
        {"name": "OCaml Documentation", "url": "https://ocaml.org/docs", "type": "official-documentation", "priority": 9},
        {"name": "Clojure Guides", "url": "https://clojure.org/guides/getting_started", "type": "official-documentation", "priority": 8},
        {"name": "Elm Guide", "url": "https://guide.elm-lang.org/", "type": "official-documentation", "priority": 8},
        {"name": "PureScript Documentation", "url": "https://www.purescript.org/documentation", "type": "official-documentation", "priority": 8},
    ],
    "lang-modern-systems": [
        {"name": "Zig Documentation", "url": "https://ziglang.org/documentation/master/", "type": "official-documentation", "priority": 9},
        {"name": "Nim Documentation", "url": "https://nim-lang.org/documentation.html", "type": "official-documentation", "priority": 8},
        {"name": "Crystal Language Reference", "url": "https://crystal-lang.org/reference/", "type": "official-documentation", "priority": 8},
        {"name": "D Language Specification", "url": "https://dlang.org/spec/spec.html", "type": "official-documentation", "priority": 8},
        {"name": "Groovy Documentation", "url": "https://groovy-lang.org/documentation.html", "type": "official-documentation", "priority": 8},
    ],
    "lang-web-frontend": [
        {"name": "WHATWG HTML Living Standard", "url": "https://html.spec.whatwg.org/multipage/", "type": "official-standard", "priority": 10},
        {"name": "MDN CSS Reference", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference", "type": "developer-reference", "priority": 9},
        {"name": "React Documentation", "url": "https://react.dev/learn", "type": "official-documentation", "priority": 9},
        {"name": "web.dev", "url": "https://web.dev/", "type": "practical-guide", "priority": 8},
    ],
    "lang-web-styling": [
        {"name": "Sass Documentation", "url": "https://sass-lang.com/documentation/", "type": "official-documentation", "priority": 9},
        {"name": "Less Documentation", "url": "https://lesscss.org/", "type": "official-documentation", "priority": 8},
        {"name": "Stylus Documentation", "url": "https://stylus-lang.com/", "type": "official-documentation", "priority": 8},
    ],
    "lang-wasm": [
        {"name": "WebAssembly", "url": "https://webassembly.org/", "type": "official-documentation", "priority": 9},
        {"name": "WebAssembly Core Specification", "url": "https://webassembly.github.io/spec/core/", "type": "official-specification", "priority": 8},
    ],
    "lang-low-level-misc": [
        {"name": "NASM Documentation", "url": "https://www.nasm.us/doc/", "type": "assembler-reference", "priority": 8},
        {"name": "GNU Fortran Documentation", "url": "https://gcc.gnu.org/onlinedocs/gfortran/", "type": "official-documentation", "priority": 8},
        {"name": "AdaCore Learn", "url": "https://learn.adacore.com/", "type": "official-documentation", "priority": 8},
        {"name": "GnuCOBOL Programmer's Guide", "url": "https://gnucobol.sourceforge.io/", "type": "official-documentation", "priority": 7},
        {"name": "SWI-Prolog Documentation", "url": "https://www.swi-prolog.org/pldoc/", "type": "official-documentation", "priority": 8},
        {"name": "Racket Documentation", "url": "https://docs.racket-lang.org/", "type": "official-documentation", "priority": 8},
    ],
    "lang-game-dev": [
        {"name": "Godot GDScript Basics", "url": "https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/", "type": "official-documentation", "priority": 9},
        {"name": "Haxe Manual", "url": "https://haxe.org/documentation/introduction/", "type": "official-documentation", "priority": 8},
        {"name": "Unreal Engine Blueprint Visual Scripting", "url": "https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprints-visual-scripting-in-unreal-engine", "type": "official-documentation", "priority": 8},
    ],
    "lang-math-stats": [
        {"name": "MATLAB Documentation", "url": "https://www.mathworks.com/help/matlab/", "type": "official-documentation", "priority": 9},
        {"name": "SAS Documentation", "url": "https://documentation.sas.com/", "type": "official-documentation", "priority": 8},
    ],
    "lang-query-data": [
        {"name": "PostgreSQL Documentation", "url": "https://www.postgresql.org/docs/", "type": "sql-reference", "priority": 9},
        {"name": "Oracle PL/SQL Language Reference", "url": "https://docs.oracle.com/en/database/oracle/oracle-database/", "type": "official-documentation", "priority": 8},
        {"name": "Microsoft Transact-SQL", "url": "https://learn.microsoft.com/en-us/sql/t-sql/language-reference", "type": "official-documentation", "priority": 8},
        {"name": "GraphQL Learn", "url": "https://graphql.org/learn/", "type": "official-documentation", "priority": 9},
        {"name": "Cypher Manual", "url": "https://neo4j.com/docs/cypher-manual/current/", "type": "official-documentation", "priority": 8},
        {"name": "SPARQL 1.2 Specification", "url": "https://www.w3.org/TR/sparql12-query/", "type": "official-specification", "priority": 8},
        {"name": "XQuery 3.1", "url": "https://www.w3.org/TR/xquery-31/", "type": "official-specification", "priority": 7},
    ],
    "lang-shell-scripting": [
        {"name": "GNU Bash Manual", "url": "https://www.gnu.org/software/bash/manual/", "type": "official-documentation", "priority": 9},
        {"name": "PowerShell Documentation", "url": "https://learn.microsoft.com/en-us/powershell/", "type": "official-documentation", "priority": 9},
        {"name": "Zsh Documentation", "url": "https://zsh.sourceforge.io/Doc/", "type": "official-documentation", "priority": 8},
        {"name": "Fish Shell Documentation", "url": "https://fishshell.com/docs/current/", "type": "official-documentation", "priority": 8},
        {"name": "Tcl Documentation", "url": "https://www.tcl.tk/doc/", "type": "official-documentation", "priority": 8},
        {"name": "GNU Awk Manual", "url": "https://www.gnu.org/software/gawk/manual/", "type": "official-documentation", "priority": 8},
        {"name": "GNU Sed Manual", "url": "https://www.gnu.org/software/sed/manual/", "type": "official-documentation", "priority": 8},
    ],
    "lang-hardware-embedded": [
        {"name": "OpenCL Overview", "url": "https://www.khronos.org/opencl/", "type": "official-documentation", "priority": 8},
        {"name": "CUDA Documentation", "url": "https://docs.nvidia.com/cuda/", "type": "official-documentation", "priority": 9},
        {"name": "Arduino Documentation", "url": "https://docs.arduino.cc/", "type": "official-documentation", "priority": 8},
        {"name": "Verilator Guide", "url": "https://verilator.org/guide/latest/", "type": "tooling-reference", "priority": 7},
    ],
    "lang-historical-academic": [
        {"name": "Mercury Documentation", "url": "https://mercurylang.org/documentation.html", "type": "official-documentation", "priority": 7},
        {"name": "Racket Documentation", "url": "https://docs.racket-lang.org/", "type": "official-documentation", "priority": 8},
        {"name": "Dyalog APL Documentation", "url": "https://help.dyalog.com/latest/", "type": "official-documentation", "priority": 7},
        {"name": "Eiffel Documentation", "url": "https://www.eiffel.org/doc/", "type": "official-documentation", "priority": 7},
        {"name": "ColdFusion Documentation", "url": "https://helpx.adobe.com/coldfusion/developing-applications.html", "type": "official-documentation", "priority": 7},
    ],
    "lang-infra-formats": [
        {"name": "YAML Specification", "url": "https://yaml.org/spec/", "type": "official-specification", "priority": 8},
        {"name": "JSON", "url": "https://www.json.org/json-en.html", "type": "reference", "priority": 7},
        {"name": "TOML", "url": "https://toml.io/en/", "type": "official-documentation", "priority": 8},
        {"name": "HashiCorp Configuration Language", "url": "https://developer.hashicorp.com/terraform/language", "type": "official-documentation", "priority": 9},
        {"name": "Dockerfile Reference", "url": "https://docs.docker.com/reference/dockerfile/", "type": "official-documentation", "priority": 9},
        {"name": "Prometheus Querying Basics", "url": "https://prometheus.io/docs/prometheus/latest/querying/basics/", "type": "official-documentation", "priority": 8},
        {"name": "Regular Expressions MDN", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions", "type": "developer-reference", "priority": 7},
        {"name": "XML", "url": "https://www.w3.org/XML/", "type": "official-documentation", "priority": 8},
        {"name": "Protocol Buffers", "url": "https://protobuf.dev/", "type": "official-documentation", "priority": 9},
    ],
}


def _now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default):
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data) -> None:
    _ensure_dirs()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _append_jsonl(path: Path, entry: dict) -> None:
    _ensure_dirs()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _normalize(text: str) -> str:
    return " ".join((text or "").lower().strip().split())


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", _normalize(value)).strip("_")


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Edit on GitHub|Report a problem with this content", "", text, flags=re.I)
    return text.strip()


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def _chunk_text(text: str, max_chars: int = 1800) -> List[str]:
    paragraphs = re.split(r"(?<=[.!?])\s+", text)
    chunks: List[str] = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(current) + len(paragraph) + 1 > max_chars:
            if current.strip():
                chunks.append(current.strip())
            current = paragraph
        else:
            current = f"{current} {paragraph}".strip()

    if current.strip():
        chunks.append(current.strip())

    return chunks


def _extract_page_text(html: str, fallback_title: str) -> Dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "canvas", "iframe"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else fallback_title

    headings = []
    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = heading.get_text(" ", strip=True)
        if text and len(text) < 180:
            headings.append(text)

    body_text = _clean_text(soup.get_text(" "))

    return {
        "title": title,
        "headings": " | ".join(headings[:50]),
        "text": body_text,
    }


def _fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return None

    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    if response.status_code != 200:
        raise RuntimeError(f"{url} returned HTTP {response.status_code}")

    return response.text


def _infer_source_groups(topic_name: str) -> List[str]:
    text = _normalize(topic_name)
    groups: List[str] = []

    keyword_groups = [
        (("computer", "computational", "algorithm", "data structure", "debugging"), "computer-foundations"),
        (("logic", "mathematics", "math", "problem solving", "learn how to learn"), "math-logic-learning"),
        (("english", "writing", "communication", "presentation", "proposal", "negotiation", "client", "stakeholder"), "english-communication"),
        (("internet", "browser", "rendering", "responsive design", "accessibility", "seo", "cdn", "dns"), "internet-web"),
        (("software", "clean code", "design pattern", "object-oriented", "functional programming", "testing", "documentation", "refactoring", "pair programming", "code review", "quality assurance"), "software-engineering"),
        (("git", "github", "version control"), "git-collaboration"),
        (("architecture", "system design", "scalability", "distributed systems", "microservices", "monolithic", "serverless", "domain-driven", "event sourcing", "saas", "multi-tenant", "erp", "crm", "lms", "pos", "marketplace", "booking"), "architecture-systems"),
        (("database", "sql", "nosql", "data model", "etl", "analytics", "big data", "orm", "replication", "sharding", "indexing"), "databases-data"),
        (("security", "owasp", "authentication", "authorization", "encryption", "ssl", "tls", "https", "threat", "bug bounty", "hacking", "malware", "forensics", "cyber"), "security-fundamentals"),
        (("docker", "kubernetes", "devops", "ci/cd", "cloud", "terraform", "infrastructure as code", "container", "deployment", "monitoring", "observability", "incident", "backup", "disaster recovery"), "devops-cloud"),
        (("linux", "windows", "macos", "operating system", "virtualization"), "operating-systems"),
        (("ui/ux", "frontend", "websocket", "real-time", "pwa"), "frontend-ux"),
        (("api", "rest", "graphql", "websocket", "backend", "payment gateway", "search engine"), "backend-api"),
        (("machine learning", "artificial intelligence", "neural network", "natural language processing", "computer vision", "recommendation", "prompt engineering", "vector database", "rag", "agent architectures"), "ai-ml"),
        (("android", "ios", "mobile", "desktop application", "cross-platform", "native android", "native ios"), "mobile-platforms"),
        (("agile", "scrum", "kanban", "project management", "product", "business", "startup", "mvp", "pricing", "customer support", "sla", "growth", "leadership", "management", "hiring", "mentorship", "consulting", "entrepreneurship", "finance", "budgeting"), "business-product"),
        (("gdpr", "pci-dss", "compliance", "legal", "privacy", "licensing"), "compliance"),
        (("penetration testing", "reverse engineering", "red team", "blue team", "ethical hacking"), "cybersecurity-advanced"),
        (("hardware", "electronics", "embedded", "iot", "robotics"), "hardware-electronics"),
    ]

    for keywords, group in keyword_groups:
        if any(keyword in text for keyword in keywords):
            groups.append(group)

    if not groups:
        groups.extend(["computer-foundations", "software-engineering"])

    return list(dict.fromkeys(groups))


def _infer_category(topic_name: str) -> str:
    groups = _infer_source_groups(topic_name)
    return groups[0] if groups else "general-learning"


def _infer_track(topic_name: str, category: str | None = None, tags: list[str] | None = None) -> str:
    text = _normalize(topic_name)
    tag_text = " ".join(_normalize(tag) for tag in (tags or []))
    haystack = f"{text} {tag_text}"
    category = _normalize(category or "")

    if any(keyword in haystack for keyword in COMPUTER_HARDWARE_KEYWORDS):
        return "computer-hardware"

    if any(keyword in haystack for keyword in SEO_KEYWORDS):
        return "seo"

    if any(keyword in haystack for keyword in DIGITAL_MARKETING_KEYWORDS):
        return "digital-marketing"

    if category in {
        "frontend",
        "framework",
        "runtime",
        "programming-language",
        "backend-api",
        "architecture-systems",
        "databases-data",
        "security-fundamentals",
        "devops-cloud",
        "operating-systems",
        "git-collaboration",
        "ai-ml",
        "mobile-platforms",
        "software-engineering",
    }:
        return "software-development"

    if any(keyword in haystack for keyword in SOFTWARE_DEVELOPMENT_KEYWORDS):
        return "software-development"

    return "rest-of-world"


def _topic_sort_key(topic: dict) -> tuple:
    track = topic.get("track") or _infer_track(topic.get("topic", ""), topic.get("category"), topic.get("tags", []))
    category = topic.get("category", "general-learning")
    version_context = topic.get("version_context") or ""
    return (
        CURRICULUM_TRACK_PRIORITY.get(track, CURRICULUM_TRACK_PRIORITY["rest-of-world"]),
        0 if version_context else 1,
        category,
        _normalize(topic.get("topic", "")),
    )


def _expand_topic_entry(topic_entry) -> dict:
    if isinstance(topic_entry, str):
        topic_name = topic_entry.strip()
        source_groups = _infer_source_groups(topic_name)
        sources = []
        for group in source_groups:
            sources.extend(SOURCE_GROUPS.get(group, []))
        deduped = []
        seen = set()
        for source in sources:
            key = (source.get("name"), source.get("url"))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(dict(source))
        return {
            "topic": topic_name,
            "aliases": [],
            "category": _infer_category(topic_name),
            "track": _infer_track(topic_name, _infer_category(topic_name), []),
            "tags": [_slugify(topic_name), "autonomous-learning"],
            "proficiency_target": "advanced-practitioner",
            "sources": deduped,
            "source_groups": source_groups,
        }

    topic = dict(topic_entry)
    if not topic.get("sources"):
        source_groups = topic.get("source_groups") or _infer_source_groups(topic.get("topic", ""))
        sources = []
        for group in source_groups:
            sources.extend(SOURCE_GROUPS.get(group, []))
        deduped = []
        seen = set()
        for source in sources:
            key = (source.get("name"), source.get("url"))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(source)
        topic["sources"] = deduped
        topic["source_groups"] = source_groups

    if not topic.get("category"):
        topic["category"] = _infer_category(topic.get("topic", ""))

    topic["track"] = topic.get("track") or _infer_track(topic.get("topic", ""), topic.get("category"), topic.get("tags", []))

    if not topic.get("proficiency_target"):
        topic["proficiency_target"] = "advanced-practitioner"

    if not topic.get("tags"):
        base_tag = "senior-engineer-curriculum" if topic["proficiency_target"] == "senior-software-engineer" else "autonomous-learning"
        topic["tags"] = [_slugify(topic.get("topic", "")), base_tag]

    if topic.get("topic", "").strip().lower() == "laravel" and not topic.get("version_context"):
        topic["version_context"] = "Laravel 12.x"
        topic.setdefault("version_policy", "Always match the project major version and use the versioned official documentation.")
        topic.setdefault("aliases", [])
        for alias in ["laravel 12", "laravel 12.x"]:
            if alias not in topic["aliases"]:
                topic["aliases"].append(alias)

    return topic


def _load_catalog() -> dict:
    programming = _load_json(CATEGORY_FILE, {"topics": []})
    senior_languages = _load_json(SENIOR_LANGUAGE_FILE, {"topics": []})
    autonomous = _load_json(AUTONOMOUS_TOPICS_FILE, {"topics": []})

    topics = [_expand_topic_entry(topic) for topic in programming.get("topics", [])]
    topics.extend(_expand_topic_entry(topic) for topic in senior_languages.get("topics", []))
    topics.extend(_expand_topic_entry(topic) for topic in autonomous.get("topics", []))

    deduped_by_topic: Dict[str, dict] = {}
    ordered_keys: List[str] = []
    for topic in topics:
        key = _normalize(topic.get("topic", ""))
        if not key:
            continue
        if key not in deduped_by_topic:
            ordered_keys.append(key)
        deduped_by_topic[key] = topic

    sorted_topics = sorted((deduped_by_topic[key] for key in ordered_keys), key=_topic_sort_key)
    return {"topics": sorted_topics}


def _topic_map() -> Dict[str, dict]:
    catalog = _load_catalog()
    mapping: Dict[str, dict] = {}

    for topic in catalog.get("topics", []):
        canonical = _normalize(topic.get("topic", ""))
        if canonical:
            mapping[canonical] = topic

        for alias in topic.get("aliases", []):
            alias_norm = _normalize(alias)
            if alias_norm:
                mapping[alias_norm] = topic

    return mapping


def list_programming_topics() -> List[str]:
    catalog = _load_catalog()
    return [topic.get("topic", "") for topic in catalog.get("topics", []) if topic.get("topic")]


def resolve_programming_topic(text: str) -> Optional[dict]:
    mapping = _topic_map()
    normalized = _normalize(text)

    if normalized in mapping:
        return mapping[normalized]

    for alias, topic in mapping.items():
        if alias and (normalized == alias or normalized.endswith(alias)):
            return topic

    return None


def _topic_query_fragment(text: str) -> str:
    normalized = _normalize(text)

    for prefix in FORCE_PREFIXES + UPDATE_PREFIXES + STATUS_PREFIXES:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):].strip()
            break

    for phrase in [
        "knowledge status",
        "status",
        "knowledge",
        "from official sources",
        "official sources",
        "automatically",
        "automation",
        "for me",
    ]:
        normalized = normalized.replace(phrase, " ")

    tokens = [token for token in normalized.split() if token not in TOPIC_STOPWORDS]
    return " ".join(tokens).strip()


def _is_all_topics_request(text: str) -> bool:
    normalized = _normalize(text)
    if any(
        normalized == alias
        or normalized.startswith(alias + " ")
        or f" {alias} " in f" {normalized} "
        for alias in ALL_TOPICS_ALIASES
    ):
        if "learn" in normalized or "update" in normalized or "refresh" in normalized or "teach yourself" in normalized:
            return True
    return False


def infer_programming_knowledge_action(user_input: str) -> dict:
    text = _normalize(user_input)
    force = any(text.startswith(prefix) for prefix in FORCE_PREFIXES) or "force" in text

    if _is_all_topics_request(text):
        return {"action": "update_all", "force": force}

    if (
        "automate" in text
        and ("learn" in text or "learning" in text)
        and ("programming" in text or "languages" in text or "frameworks" in text or "topics" in text or "curriculum" in text)
    ):
        return {"action": "update_all", "force": force}

    if text in {
        "programming knowledge status",
        "programming languages status",
        "teaching session status",
        "learning curriculum status",
        "autonomous learning status",
    }:
        return {"action": "status_all"}

    if text.startswith(tuple(UPDATE_PREFIXES + FORCE_PREFIXES)):
        topic = resolve_programming_topic(text)
        if topic:
            return {"action": "update", "force": force, "topic": topic.get("topic")}

        fragment = _topic_query_fragment(text)
        topic = resolve_programming_topic(fragment)
        if topic:
            return {"action": "update", "force": force, "topic": topic.get("topic")}

    if "status" in text or "check" in text or "show" in text:
        topic = resolve_programming_topic(text)
        if topic:
            return {"action": "status", "topic": topic.get("topic")}

        fragment = _topic_query_fragment(text)
        topic = resolve_programming_topic(fragment)
        if topic:
            return {"action": "status", "topic": topic.get("topic")}

    return {"action": "unknown"}


def _manifest_path(topic_name: str) -> Path:
    return MANIFEST_DIR / f"{_slugify(topic_name)}_knowledge_manifest.json"


def _log_learning_event(entry: dict) -> None:
    _append_jsonl(LOG_FILE, entry)


def _learn_topic(topic_config: dict, force: bool = False, trigger: str = "manual") -> dict:
    _ensure_dirs()

    topic_name = topic_config.get("topic", "unknown")
    proficiency_target = topic_config.get("proficiency_target", "advanced-practitioner")
    manifest_path = _manifest_path(topic_name)
    manifest = _load_json(manifest_path, {"updated_at": None, "topic": topic_name, "sources": {}})
    manifest_sources = manifest.setdefault("sources", {})

    total_chunks = 0
    updated_sources = 0
    skipped_sources = 0
    errors: List[str] = []
    started_at = _now_iso()

    for source in topic_config.get("sources", []):
        name = source.get("name", "Unnamed source")
        url = source.get("url")
        source_type = source.get("type", "reference")
        priority = int(source.get("priority", 5))

        if not url:
            continue

        try:
            html = _fetch_url(url)
            extracted = _extract_page_text(html or "", f"Untitled {topic_name.title()} Source")
            text = extracted["text"]
            digest = _content_hash(text)

            old_digest = manifest_sources.get(url, {}).get("hash")
            if old_digest == digest and not force:
                skipped_sources += 1
                continue

            chunks = _chunk_text(text)

            for index, chunk in enumerate(chunks):
                memory_text = (
                    f"{topic_name.upper()} KNOWLEDGE SOURCE\n"
                    f"Learning target: {proficiency_target}\n"
                    f"Source name: {name}\n"
                    f"Source type: {source_type}\n"
                    f"URL: {url}\n"
                    f"Page title: {extracted['title']}\n"
                    f"Headings: {extracted['headings']}\n"
                    f"Chunk: {index + 1}/{len(chunks)}\n\n"
                    f"{chunk}"
                )

                add_vector_memory(
                    memory_text,
                    tags=list(dict.fromkeys([
                        _slugify(topic_name),
                        "programming",
                        topic_config.get("category", "general-programming"),
                        *topic_config.get("tags", []),
                        source_type,
                    ])),
                    source=f"{_slugify(topic_name)}-knowledge-engine",
                    importance=priority,
                )
                total_chunks += 1

            manifest_sources[url] = {
                "name": name,
                "type": source_type,
                "priority": priority,
                "hash": digest,
                "last_learned_at": _now_iso(),
                "chunks_saved": len(chunks),
                "title": extracted["title"],
            }
            updated_sources += 1
            time.sleep(1)
        except Exception as exc:
            errors.append(f"{name}: {exc}")

    manifest["updated_at"] = _now_iso()
    manifest["topic"] = topic_name
    manifest["category"] = topic_config.get("category", "general-programming")
    manifest["version"] = topic_config.get("version", "1.0.0")
    manifest["proficiency_target"] = proficiency_target
    _save_json(manifest_path, manifest)

    result = {
        "topic": topic_name,
        "proficiency_target": proficiency_target,
        "trigger": trigger,
        "force": force,
        "started_at": started_at,
        "completed_at": _now_iso(),
        "sources_updated": updated_sources,
        "sources_skipped": skipped_sources,
        "memory_chunks_saved": total_chunks,
        "errors": errors,
        "manifest_path": str(manifest_path),
    }
    _log_learning_event(result)
    return result


def update_programming_topic(topic_name: str, force: bool = False, trigger: str = "manual") -> str:
    topic = resolve_programming_topic(topic_name)
    if not topic:
        available = ", ".join(list_programming_topics())
        return (
            "AUTONOMOUS LEARNING UPDATE FAILED\n"
            f"Unknown topic: {topic_name}\n"
            f"Available topics: {available}"
        )

    result = _learn_topic(topic, force=force, trigger=trigger)
    lines = [
        f"{topic['topic'].upper()} KNOWLEDGE UPDATE COMPLETE",
        f"Sources updated: {result['sources_updated']}",
        f"Sources skipped: {result['sources_skipped']}",
        f"Memory chunks saved: {result['memory_chunks_saved']}",
        f"Manifest: {result['manifest_path']}",
        f"Log: {LOG_FILE}",
    ]

    if result["errors"]:
        lines.append("")
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in result["errors"][:10])

    return "\n".join(lines)


def update_all_programming_knowledge(force: bool = False, trigger: str = "manual") -> str:
    catalog = _load_catalog()
    topics = [topic for topic in catalog.get("topics", []) if topic.get("topic")]

    if not topics:
        return (
            "AUTONOMOUS LEARNING UPDATE FAILED\n"
            "Missing configured learning topics."
        )

    batch_started_at = _now_iso()
    summaries = []
    total_updated = 0
    total_skipped = 0
    total_chunks = 0
    total_errors = 0

    for topic in topics:
        result = _learn_topic(topic, force=force, trigger=trigger)
        summaries.append(result)
        total_updated += result["sources_updated"]
        total_skipped += result["sources_skipped"]
        total_chunks += result["memory_chunks_saved"]
        total_errors += len(result["errors"])

    _log_learning_event({
        "type": "batch_programming_learning",
        "trigger": trigger,
        "force": force,
        "started_at": batch_started_at,
        "completed_at": _now_iso(),
        "topics": [summary["topic"] for summary in summaries],
        "sources_updated": total_updated,
        "sources_skipped": total_skipped,
        "memory_chunks_saved": total_chunks,
        "error_count": total_errors,
    })

    lines = [
        "AUTONOMOUS LEARNING UPDATE COMPLETE",
        f"Topics processed: {len(summaries)}",
        f"Sources updated: {total_updated}",
        f"Sources skipped: {total_skipped}",
        f"Memory chunks saved: {total_chunks}",
        f"Learning log: {LOG_FILE}",
        "",
        "Topics:",
    ]
    lines.extend(
        f"- {summary['topic']}: {summary['sources_updated']} updated, {summary['memory_chunks_saved']} chunks"
        for summary in summaries
    )

    if total_errors:
        lines.append("")
        lines.append(f"Topics with errors: {total_errors}")

    return "\n".join(lines)


def programming_knowledge_status(topic_name: Optional[str] = None) -> str:
    if topic_name:
        topic = resolve_programming_topic(topic_name)
        if not topic:
            return (
                "AUTONOMOUS LEARNING STATUS FAILED\n"
                f"Unknown topic: {topic_name}"
            )

        manifest = _load_json(_manifest_path(topic["topic"]), {"sources": {}})
        sources = manifest.get("sources", {})
        lines = [f"{topic['topic'].upper()} KNOWLEDGE STATUS"]
        lines.append(f"Last updated: {manifest.get('updated_at', '-')}")

        if not sources:
            lines.append("No learning manifest exists yet.")
            lines.append(f"Run: learn {topic['topic']}")
            return "\n".join(lines)

        for url, item in sources.items():
            lines.append("")
            lines.append(f"Source: {item.get('name', 'Unknown')}")
            lines.append(f"URL: {url}")
            lines.append(f"Last learned: {item.get('last_learned_at', '-')}")
            lines.append(f"Chunks saved: {item.get('chunks_saved', 0)}")

        lines.append("")
        lines.append(f"Log file: {LOG_FILE}")
        return "\n".join(lines)

    lines = ["AUTONOMOUS LEARNING STATUS"]
    for topic_name in list_programming_topics():
        manifest = _load_json(_manifest_path(topic_name), {"sources": {}})
        sources = manifest.get("sources", {})
        lines.append("")
        lines.append(f"Topic: {topic_name}")
        lines.append(f"Last updated: {manifest.get('updated_at', '-')}")
        lines.append(f"Sources learned: {len(sources)}")

    lines.append("")
    lines.append(f"Log file: {LOG_FILE}")
    return "\n".join(lines)
