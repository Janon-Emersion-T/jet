from pathlib import Path

from tools.content_assistant_tools import website_content_pack


def patch_bootstrap_for_admin(project_dir: Path) -> None:
    bootstrap = project_dir / "bootstrap" / "app.php"
    if not bootstrap.exists():
        return

    content = bootstrap.read_text(encoding="utf-8")
    if "EnsureUserIsAdmin" in content:
        return

    original = """    ->withMiddleware(function (Middleware $middleware): void {\n        //\n    })"""
    replacement = """    ->withMiddleware(function (Middleware $middleware): void {\n        $middleware->alias([\n            'admin' => \\App\\Http\\Middleware\\EnsureUserIsAdmin::class,\n        ]);\n    })"""

    if original in content:
        bootstrap.write_text(content.replace(original, replacement), encoding="utf-8")


def build_laravel_content_platform_files(company_name: str) -> dict[str, str]:
    content_pack = website_content_pack(company_name)
    company_display = " ".join((company_name or "").split()).strip() or "Center for Systematic Learning"

    files: dict[str, str] = {
        "app/Http/Middleware/EnsureUserIsAdmin.php": """<?php

namespace App\\Http\\Middleware;

use Closure;
use Illuminate\\Http\\Request;
use Symfony\\Component\\HttpFoundation\\Response;

class EnsureUserIsAdmin
{
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user() || ! $request->user()->is_admin) {
            abort(403, 'Admin access only.');
        }

        return $next($request);
    }
}
""",
        "app/Models/BlogPost.php": """<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Database\\Eloquent\\Model;

class BlogPost extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        'slug',
        'excerpt',
        'content',
        'is_published',
        'published_at',
    ];

    protected function casts(): array
    {
        return [
            'is_published' => 'boolean',
            'published_at' => 'datetime',
        ];
    }

    public function scopePublished($query)
    {
        return $query
            ->where('is_published', true)
            ->whereNotNull('published_at');
    }
}
""",
        "app/Http/Controllers/PageController.php": f"""<?php

namespace App\\Http\\Controllers;

use App\\Models\\BlogPost;
use Illuminate\\Http\\RedirectResponse;
use Illuminate\\Http\\Request;
use Illuminate\\View\\View;

class PageController extends Controller
{{
    public function home(): View
    {{
        return view('pages.home', [
            'featuredPosts' => BlogPost::published()->latest('published_at')->take(3)->get(),
        ]);
    }}

    public function about(): View
    {{
        return view('pages.about');
    }}

    public function media(): View
    {{
        return view('pages.media');
    }}

    public function contact(): View
    {{
        return view('pages.contact');
    }}

    public function submitContact(Request $request): RedirectResponse
    {{
        $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'max:255'],
            'message' => ['required', 'string', 'min:20'],
        ]);

        return back()->with('status', 'Thanks. Your inquiry has been captured for follow-up.');
    }}
}}
""",
        "app/Http/Controllers/BlogController.php": """<?php

namespace App\\Http\\Controllers;

use App\\Models\\BlogPost;
use Illuminate\\View\\View;

class BlogController extends Controller
{
    public function index(): View
    {
        return view('pages.blogs.index', [
            'blogPosts' => BlogPost::published()->latest('published_at')->paginate(9),
        ]);
    }

    public function show(BlogPost $blogPost): View
    {
        abort_unless($blogPost->is_published, 404);

        return view('pages.blogs.show', [
            'blogPost' => $blogPost,
        ]);
    }
}
""",
        "app/Http/Controllers/Admin/DashboardController.php": """<?php

namespace App\\Http\\Controllers\\Admin;

use App\\Http\\Controllers\\Controller;
use App\\Models\\BlogPost;
use App\\Models\\User;
use Illuminate\\View\\View;

class DashboardController extends Controller
{
    public function __invoke(): View
    {
        return view('admin.dashboard', [
            'blogCount' => BlogPost::count(),
            'publishedCount' => BlogPost::where('is_published', true)->count(),
            'adminCount' => User::where('is_admin', true)->count(),
            'latestPosts' => BlogPost::latest()->take(5)->get(),
        ]);
    }
}
""",
        "app/Http/Controllers/Admin/BlogPostController.php": """<?php

namespace App\\Http\\Controllers\\Admin;

use App\\Http\\Controllers\\Controller;
use App\\Models\\BlogPost;
use Illuminate\\Http\\RedirectResponse;
use Illuminate\\Http\\Request;
use Illuminate\\Support\\Str;
use Illuminate\\Validation\\Rule;
use Illuminate\\View\\View;

class BlogPostController extends Controller
{
    public function index(): View
    {
        return view('admin.blogs.index', [
            'blogPosts' => BlogPost::latest()->paginate(10),
        ]);
    }

    public function create(): View
    {
        return view('admin.blogs.form', [
            'blogPost' => new BlogPost(),
            'mode' => 'create',
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $data = $this->validated($request);
        $data['slug'] = $data['slug'] ?: Str::slug($data['title']);

        BlogPost::create($data);

        return redirect()->route('admin.blogs.index')->with('status', 'Blog post created.');
    }

    public function edit(BlogPost $blogPost): View
    {
        return view('admin.blogs.form', [
            'blogPost' => $blogPost,
            'mode' => 'edit',
        ]);
    }

    public function update(Request $request, BlogPost $blogPost): RedirectResponse
    {
        $data = $this->validated($request, $blogPost);
        $data['slug'] = $data['slug'] ?: Str::slug($data['title']);

        $blogPost->update($data);

        return redirect()->route('admin.blogs.index')->with('status', 'Blog post updated.');
    }

    public function destroy(BlogPost $blogPost): RedirectResponse
    {
        $blogPost->delete();

        return redirect()->route('admin.blogs.index')->with('status', 'Blog post deleted.');
    }

    private function validated(Request $request, ?BlogPost $blogPost = null): array
    {
        return $request->validate([
            'title' => ['required', 'string', 'max:255'],
            'slug' => ['nullable', 'string', 'max:255', Rule::unique('blog_posts', 'slug')->ignore($blogPost?->id)],
            'excerpt' => ['nullable', 'string', 'max:500'],
            'content' => ['required', 'string', 'min:60'],
            'published_at' => ['nullable', 'date'],
            'is_published' => ['nullable', 'boolean'],
        ]) + [
            'is_published' => $request->boolean('is_published'),
        ];
    }
}
""",
        "database/migrations/2026_06_02_000100_add_is_admin_to_users_table.php": """<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->boolean('is_admin')->default(false)->after('email');
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('is_admin');
        });
    }
};
""",
        "database/migrations/2026_06_02_000200_create_blog_posts_table.php": """<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('blog_posts', function (Blueprint $table) {
            $table->id();
            $table->string('title');
            $table->string('slug')->unique();
            $table->text('excerpt')->nullable();
            $table->longText('content');
            $table->boolean('is_published')->default(false);
            $table->timestamp('published_at')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('blog_posts');
    }
};
""",
        "database/seeders/DatabaseSeeder.php": """<?php

namespace Database\\Seeders;

use App\\Models\\BlogPost;
use App\\Models\\User;
use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\Hash;
use Illuminate\\Support\\Str;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        User::updateOrCreate(
            ['email' => 'janonemersion@hotmail.com'],
            [
                'name' => 'Janon Emersion',
                'password' => Hash::make('Jj112112@!@!'),
                'is_admin' => true,
                'email_verified_at' => now(),
            ]
        );

        $posts = [
            [
                'title' => 'Why Systematic Learning Outperforms Random Motivation',
                'excerpt' => 'A practical argument for building real learning systems instead of relying on short bursts of inspiration.',
                'content' => 'Strong learning systems win because they remove guesswork. Instead of depending on motivation alone, they create sequence, repetition, and visible progress. That changes the learner experience from chaotic to confident.\\n\\nFor institutions, this means better transfer into work. For individuals, it means less wasted energy. Systematic learning is not about making things rigid. It is about making growth dependable.',
            ],
            [
                'title' => 'How Better Resource People Improve Learning Outcomes',
                'excerpt' => 'The right resource person does more than speak well. They structure insight, practice, and reflection.',
                'content' => 'A strong resource person helps learners think more clearly, not just listen politely. They translate complex ideas into useful mental models, examples, and exercises that people can actually apply.\\n\\nThis is why institutions should choose resource people based on teaching quality, domain credibility, and the ability to make difficult topics feel workable.',
            ],
            [
                'title' => 'Designing Blog Content That Teaches, Not Just Attracts Clicks',
                'excerpt' => 'Educational brands need publishing systems that build trust through clarity and substance.',
                'content' => 'A serious educational blog should do more than chase traffic. It should help readers understand, compare, and act. That means clear titles, grounded explanations, structured examples, and a tone that respects the audience.\\n\\nWhen publishing becomes part of the teaching system, blog content starts compounding value instead of disappearing after a single post.',
            ],
            [
                'title' => 'Why Institutions Need a Learning Dashboard',
                'excerpt' => 'Dashboards are not just for metrics. They create operational clarity around programs, content, and momentum.',
                'content' => 'A good learning dashboard helps teams see what has been created, what is published, what is still in progress, and where attention is needed next. It turns scattered activity into operational visibility.\\n\\nThat visibility matters because learning programs involve content, schedules, people, and follow-through. A clear dashboard gives leaders a way to steer with confidence.',
            ],
            [
                'title' => 'Making Media Part of the Learning Experience',
                'excerpt' => 'Lectures, clips, recordings, and public resources should reinforce the curriculum instead of sitting alone.',
                'content' => 'Media becomes more powerful when it is designed as part of the larger learning system. A lecture can introduce the concept, a short video can reinforce it, and a downloadable guide can help the learner apply it later.\\n\\nThis approach extends the life of teaching and gives institutions a richer library of assets that keep working after the live session ends.',
            ],
        ];

        foreach ($posts as $index => $post) {
            BlogPost::updateOrCreate(
                ['slug' => Str::slug($post['title'])],
                [
                    'title' => $post['title'],
                    'excerpt' => $post['excerpt'],
                    'content' => $post['content'],
                    'is_published' => true,
                    'published_at' => now()->subDays(5 - $index),
                ]
            );
        }
    }
}
""",
        "resources/views/layouts/public.blade.php": f"""<!DOCTYPE html>
<html lang="{{{{ str_replace('_', '-', app()->getLocale()) }}}}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title', '{company_display}')</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="min-h-screen bg-slate-950 text-slate-100 antialiased">
    <div class="absolute inset-x-0 top-0 -z-10 h-[28rem] bg-[radial-gradient(circle_at_top,rgba(34,197,94,0.18),transparent_35%),linear-gradient(180deg,#020617_0%,#0f172a_70%,#e2e8f0_70%,#e2e8f0_100%)]"></div>
    <header class="sticky top-0 z-40 border-b border-white/10 bg-slate-950/85 backdrop-blur">
        <div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-10">
            <a href="{{{{ route('home') }}}}" class="flex items-center gap-3">
                <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-400/15 text-sm font-bold text-emerald-300">CSL</div>
                <div>
                    <p class="text-xs uppercase tracking-[0.3em] text-slate-400">Learning System</p>
                    <p class="text-lg font-semibold text-white">{company_display}</p>
                </div>
            </a>
            <nav class="hidden items-center gap-2 lg:flex">
                <a href="{{{{ route('home') }}}}" class="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/10 hover:text-white">Home</a>
                <a href="{{{{ route('about') }}}}" class="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/10 hover:text-white">About Us</a>
                <a href="{{{{ route('media') }}}}" class="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/10 hover:text-white">Media</a>
                <a href="{{{{ route('blogs.index') }}}}" class="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/10 hover:text-white">Blog</a>
                <a href="{{{{ route('contact') }}}}" class="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/10 hover:text-white">Contact Us</a>
            </nav>
            <a href="{{{{ route('login') }}}}" class="rounded-full bg-emerald-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-300">Admin Login</a>
        </div>
    </header>

    <main>
        @if (session('status'))
            <div class="mx-auto mt-6 max-w-7xl px-6 lg:px-10">
                <div class="rounded-2xl border border-emerald-400/30 bg-emerald-400/10 px-4 py-3 text-sm text-emerald-100">{{{{ session('status') }}}}</div>
            </div>
        @endif

        @yield('content')
    </main>

    <footer class="border-t border-slate-200 bg-slate-100 text-slate-800">
        <div class="mx-auto grid max-w-7xl gap-10 px-6 py-14 lg:grid-cols-4 lg:px-10">
            <div class="lg:col-span-2">
                <p class="text-xs font-semibold uppercase tracking-[0.3em] text-emerald-700">Center for Systematic Learning</p>
                <h2 class="mt-4 text-3xl font-semibold text-slate-950">{content_pack["footer_tagline"]}</h2>
                <p class="mt-4 max-w-2xl text-base leading-7 text-slate-600">{content_pack["footer_body"]}</p>
            </div>
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Explore</p>
                <ul class="mt-4 space-y-3 text-sm text-slate-700">
                    <li><a href="{{{{ route('about') }}}}" class="hover:text-emerald-700">About Us</a></li>
                    <li><a href="{{{{ route('media') }}}}" class="hover:text-emerald-700">Media</a></li>
                    <li><a href="{{{{ route('blogs.index') }}}}" class="hover:text-emerald-700">Blog</a></li>
                    <li><a href="{{{{ route('contact') }}}}" class="hover:text-emerald-700">Contact Us</a></li>
                </ul>
            </div>
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Contact</p>
                <ul class="mt-4 space-y-3 text-sm text-slate-700">
                    <li>janonemersion@hotmail.com</li>
                    <li>+94 11 245 7788</li>
                    <li>Colombo, Sri Lanka</li>
                    <li>Mon to Fri, 9:00 AM to 6:00 PM</li>
                </ul>
            </div>
        </div>
    </footer>
</body>
</html>
""",
        "resources/views/layouts/admin.blade.php": f"""<!DOCTYPE html>
<html lang="{{{{ str_replace('_', '-', app()->getLocale()) }}}}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title', 'Admin Dashboard')</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="min-h-screen bg-slate-950 text-slate-100 antialiased">
    <div class="flex min-h-screen">
        <aside class="hidden w-72 flex-col border-r border-white/10 bg-slate-950 px-6 py-8 lg:flex">
            <div class="mb-10">
                <p class="text-xs uppercase tracking-[0.3em] text-emerald-300">Admin Workspace</p>
                <h1 class="mt-3 text-2xl font-semibold text-white">{company_display}</h1>
            </div>
            <nav class="space-y-2">
                <a href="{{{{ route('admin.dashboard') }}}}" class="block rounded-2xl px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/10">Dashboard</a>
                <a href="{{{{ route('admin.blogs.index') }}}}" class="block rounded-2xl px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/10">Manage Blogs</a>
                <a href="{{{{ route('home') }}}}" class="block rounded-2xl px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/10">View Website</a>
            </nav>
            <div class="mt-auto rounded-3xl border border-white/10 bg-white/5 p-5">
                <p class="text-sm font-semibold text-white">Signed in as admin</p>
                <p class="mt-2 text-sm text-slate-400">Use this dashboard to monitor content, publish updates, and keep the site active.</p>
            </div>
        </aside>

        <div class="flex-1">
            <header class="border-b border-white/10 bg-slate-900/75 px-6 py-4 backdrop-blur lg:px-8">
                <div class="flex items-center justify-between gap-4">
                    <div>
                        <p class="text-sm uppercase tracking-[0.24em] text-slate-400">@yield('eyebrow', 'Admin')</p>
                        <h2 class="text-2xl font-semibold text-white">@yield('heading', 'Dashboard')</h2>
                    </div>
                    <form method="POST" action="{{{{ route('logout') }}}}">
                        @csrf
                        <button type="submit" class="rounded-full border border-white/10 px-4 py-2 text-sm font-medium text-white transition hover:bg-white/10">Logout</button>
                    </form>
                </div>
            </header>

            <main class="px-6 py-8 lg:px-8">
                @if (session('status'))
                    <div class="mb-6 rounded-2xl border border-emerald-400/30 bg-emerald-400/10 px-4 py-3 text-sm text-emerald-100">{{{{ session('status') }}}}</div>
                @endif
                @yield('content')
            </main>
        </div>
    </div>
</body>
</html>
""",
        "resources/views/pages/home.blade.php": f"""@extends('layouts.public')

@section('title', '{company_display} | Home')

@section('content')
    <section class="mx-auto max-w-7xl px-6 pb-24 pt-16 lg:px-10 lg:pb-28 lg:pt-24">
        <div class="grid gap-12 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
            <div class="space-y-8">
                <span class="inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.28em] text-emerald-200">{content_pack["hero_kicker"]}</span>
                <div class="space-y-6">
                    <h1 class="max-w-4xl text-5xl font-semibold leading-tight text-white sm:text-6xl">{content_pack["hero_title"]}</h1>
                    <p class="max-w-2xl text-lg leading-8 text-slate-300">{content_pack["hero_body"]}</p>
                </div>
                <div class="flex flex-col gap-4 sm:flex-row">
                    <a href="{{{{ route('contact') }}}}" class="inline-flex items-center justify-center rounded-full bg-emerald-400 px-6 py-3.5 text-sm font-semibold text-slate-950 transition hover:bg-emerald-300">{content_pack["hero_cta"]}</a>
                    <a href="{{{{ route('about') }}}}" class="inline-flex items-center justify-center rounded-full border border-white/15 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-white/10">{content_pack["hero_secondary_cta"]}</a>
                </div>
            </div>
            <div class="grid gap-4 rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/30 backdrop-blur sm:grid-cols-2">
                <div class="rounded-3xl bg-emerald-400/15 p-5">
                    <p class="text-sm uppercase tracking-[0.24em] text-emerald-200">Programs</p>
                    <p class="mt-3 text-2xl font-semibold text-white">Structured learning journeys</p>
                </div>
                <div class="rounded-3xl bg-white/8 p-5">
                    <p class="text-sm uppercase tracking-[0.24em] text-slate-300">Resource Persons</p>
                    <p class="mt-3 text-2xl font-semibold text-white">Experts who teach with clarity</p>
                </div>
                <div class="rounded-3xl bg-white/8 p-5">
                    <p class="text-sm uppercase tracking-[0.24em] text-slate-300">Media</p>
                    <p class="mt-3 text-2xl font-semibold text-white">Knowledge assets that keep working</p>
                </div>
                <div class="rounded-3xl bg-emerald-400/15 p-5">
                    <p class="text-sm uppercase tracking-[0.24em] text-emerald-200">Outcomes</p>
                    <p class="mt-3 text-2xl font-semibold text-white">Learning that transfers into real work</p>
                </div>
            </div>
        </div>
    </section>

    <section class="bg-slate-100 py-24 text-slate-900">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">
            <div class="grid gap-8 lg:grid-cols-3">
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">01. Diagnose</p>
                    <h2 class="mt-4 text-3xl font-semibold text-slate-950">Identify the real capability gap.</h2>
                    <p class="mt-4 text-base leading-7 text-slate-600">We start with context, learner needs, and real-world constraints so the solution is precise instead of generic.</p>
                </article>
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">02. Design</p>
                    <h2 class="mt-4 text-3xl font-semibold text-slate-950">Sequence the learning properly.</h2>
                    <p class="mt-4 text-base leading-7 text-slate-600">Content is structured around foundations, guided practice, review, and reinforcement so growth becomes durable.</p>
                </article>
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">03. Sustain</p>
                    <h2 class="mt-4 text-3xl font-semibold text-slate-950">Turn sessions into a learning system.</h2>
                    <p class="mt-4 text-base leading-7 text-slate-600">Dashboards, media, and publishing workflows make the learning effort reusable instead of one-time only.</p>
                </article>
            </div>
        </div>
    </section>

    <section class="bg-slate-100 pb-24 text-slate-900">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">
            <div class="flex items-end justify-between gap-6">
                <div>
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">Featured Insights</p>
                    <h2 class="mt-3 text-3xl font-semibold text-slate-950">Recent blog posts from the learning team</h2>
                </div>
                <a href="{{{{ route('blogs.index') }}}}" class="text-sm font-semibold text-emerald-700">View all posts</a>
            </div>
            <div class="mt-8 grid gap-6 lg:grid-cols-3">
                @forelse ($featuredPosts as $post)
                    <article class="rounded-[2rem] bg-white p-6 shadow-sm ring-1 ring-slate-200">
                        <p class="text-sm text-slate-500">{{{{ optional($post->published_at)->format('M d, Y') }}}}</p>
                        <h3 class="mt-3 text-2xl font-semibold text-slate-950">{{{{ $post->title }}}}</h3>
                        <p class="mt-4 text-base leading-7 text-slate-600">{{{{ $post->excerpt }}}}</p>
                        <a href="{{{{ route('blogs.show', $post) }}}}" class="mt-6 inline-flex text-sm font-semibold text-emerald-700">Read article</a>
                    </article>
                @empty
                    <p class="text-base text-slate-600">Blog posts will appear here once they are published.</p>
                @endforelse
            </div>
        </div>
    </section>
@endsection
""",
        "resources/views/pages/about.blade.php": f"""@extends('layouts.public')

@section('title', '{company_display} | About Us')

@section('content')
    <section class="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
        <div class="grid gap-10 lg:grid-cols-[0.9fr_1.1fr]">
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.28em] text-emerald-300">About Us</p>
                <h1 class="mt-5 text-5xl font-semibold leading-tight text-white">We design learning like a serious operating system for growth.</h1>
            </div>
            <div class="space-y-6 text-lg leading-8 text-slate-300">
                <p>{content_pack["about_intro"]}</p>
                <p>Our work combines curriculum structure, expert facilitation, publishing discipline, and practical delivery systems so that training feels deliberate from start to finish.</p>
            </div>
        </div>
    </section>

    <section class="bg-slate-100 py-24 text-slate-900">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">
            <div class="grid gap-8 lg:grid-cols-3">
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">Mission</p>
                    <p class="mt-4 text-lg leading-8 text-slate-700">Help people and institutions learn with more depth, stronger structure, and better real-world transfer.</p>
                </article>
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">Method</p>
                    <p class="mt-4 text-lg leading-8 text-slate-700">Use sequence, guided practice, reflection, and publishing systems to make knowledge easier to retain and use.</p>
                </article>
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">Promise</p>
                    <p class="mt-4 text-lg leading-8 text-slate-700">Clarity without oversimplification, and systems that respect both quality and execution speed.</p>
                </article>
            </div>
        </div>
    </section>
@endsection
""",
        "resources/views/pages/media.blade.php": """@extends('layouts.public')

@section('title', 'Media')

@section('content')
    <section class="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
        <div class="max-w-3xl">
            <p class="text-sm font-semibold uppercase tracking-[0.28em] text-emerald-300">Media</p>
            <h1 class="mt-5 text-5xl font-semibold leading-tight text-white">Knowledge assets that keep teaching after the session ends.</h1>
            <p class="mt-6 text-lg leading-8 text-slate-300">Lectures, interviews, event clips, and resource libraries should extend the value of your teaching instead of disappearing after one event.</p>
        </div>
    </section>

    <section class="bg-slate-100 py-24 text-slate-900">
        <div class="mx-auto grid max-w-7xl gap-8 px-6 lg:grid-cols-3 lg:px-10">
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">Featured Lectures</p>
                <h2 class="mt-4 text-3xl font-semibold text-slate-950">Programs that explain difficult ideas with structure.</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">Use this section for flagship talks, signature workshops, and recorded knowledge sessions.</p>
            </article>
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">Interviews</p>
                <h2 class="mt-4 text-3xl font-semibold text-slate-950">Conversations with experts and resource persons.</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">Highlight expert commentary, partnerships, and public educational content that reinforces the brand.</p>
            </article>
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">Resource Library</p>
                <h2 class="mt-4 text-3xl font-semibold text-slate-950">Slides, recordings, and downloadable learning tools.</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">Build a library that helps learners revisit material and keeps the institution visibly useful over time.</p>
            </article>
        </div>
    </section>
@endsection
""",
        "resources/views/pages/contact.blade.php": f"""@extends('layouts.public')

@section('title', '{company_display} | Contact Us')

@section('content')
    <section class="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
        <div class="grid gap-10 lg:grid-cols-[0.8fr_1.2fr]">
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.28em] text-emerald-300">Contact Us</p>
                <h1 class="mt-5 text-5xl font-semibold leading-tight text-white">Start a conversation about better learning systems.</h1>
                <p class="mt-6 text-lg leading-8 text-slate-300">{content_pack["contact_intro"]}</p>
                <div class="mt-8 space-y-3 text-sm text-slate-300">
                    <p><span class="font-semibold text-white">Email:</span> janonemersion@hotmail.com</p>
                    <p><span class="font-semibold text-white">Phone:</span> +94 11 245 7788</p>
                    <p><span class="font-semibold text-white">Office:</span> Colombo, Sri Lanka</p>
                </div>
            </div>
            <form method="POST" action="{{{{ route('contact.submit') }}}}" class="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-2xl shadow-black/20 backdrop-blur">
                @csrf
                <div class="grid gap-6">
                    <div>
                        <label for="name" class="mb-2 block text-sm font-medium text-slate-200">Name</label>
                        <input id="name" name="name" value="{{{{ old('name') }}}}" class="w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 text-white outline-none ring-0 placeholder:text-slate-500" required>
                    </div>
                    <div>
                        <label for="email" class="mb-2 block text-sm font-medium text-slate-200">Email</label>
                        <input id="email" type="email" name="email" value="{{{{ old('email') }}}}" class="w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 text-white outline-none ring-0 placeholder:text-slate-500" required>
                    </div>
                    <div>
                        <label for="message" class="mb-2 block text-sm font-medium text-slate-200">Message</label>
                        <textarea id="message" name="message" rows="6" class="w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 text-white outline-none ring-0 placeholder:text-slate-500" required>{{{{ old('message') }}}}</textarea>
                    </div>
                    <button type="submit" class="inline-flex items-center justify-center rounded-full bg-emerald-400 px-6 py-3.5 text-sm font-semibold text-slate-950 transition hover:bg-emerald-300">Send Inquiry</button>
                </div>
            </form>
        </div>
    </section>
@endsection
""",
        "resources/views/pages/blogs/index.blade.php": """@extends('layouts.public')

@section('title', 'Blog')

@section('content')
    <section class="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
        <div class="grid gap-10 lg:grid-cols-[0.9fr_1.1fr]">
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.28em] text-emerald-300">Blog</p>
                <h1 class="mt-5 text-5xl font-semibold leading-tight text-white">Thoughtful articles for people building serious learning experiences.</h1>
            </div>
            <p class="text-lg leading-8 text-slate-300">This blog is dynamic and database-backed, so Jarvis can seed content, manage posts in the dashboard, and keep the public publishing flow active.</p>
        </div>
    </section>

    <section class="bg-slate-100 py-24 text-slate-900">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">
            <div class="grid gap-8 lg:grid-cols-3">
                @foreach ($blogPosts as $post)
                    <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                        <p class="text-sm text-slate-500">{{ optional($post->published_at)->format('M d, Y') }}</p>
                        <h2 class="mt-4 text-3xl font-semibold text-slate-950">{{ $post->title }}</h2>
                        <p class="mt-4 text-base leading-7 text-slate-600">{{ $post->excerpt }}</p>
                        <a href="{{ route('blogs.show', $post) }}" class="mt-6 inline-flex text-sm font-semibold text-emerald-700">Read more</a>
                    </article>
                @endforeach
            </div>
            <div class="mt-10">
                {{ $blogPosts->links() }}
            </div>
        </div>
    </section>
@endsection
""",
        "resources/views/pages/blogs/show.blade.php": """@extends('layouts.public')

@section('title', $blogPost->title)

@section('content')
    <section class="mx-auto max-w-4xl px-6 py-20 lg:px-10 lg:py-24">
        <p class="text-sm font-semibold uppercase tracking-[0.28em] text-emerald-300">Blog</p>
        <h1 class="mt-5 text-5xl font-semibold leading-tight text-white">{{ $blogPost->title }}</h1>
        <p class="mt-4 text-sm text-slate-400">{{ optional($blogPost->published_at)->format('M d, Y') }}</p>
        <p class="mt-8 text-xl leading-8 text-slate-300">{{ $blogPost->excerpt }}</p>
    </section>

    <section class="bg-slate-100 py-20 text-slate-900">
        <article class="mx-auto max-w-4xl px-6 lg:px-10">
            <div class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <div class="whitespace-pre-line text-lg leading-8 text-slate-700">{{ $blogPost->content }}</div>
            </div>
        </article>
    </section>
@endsection
""",
        "resources/views/admin/dashboard.blade.php": """@extends('layouts.admin')

@section('title', 'Admin Dashboard')
@section('eyebrow', 'Overview')
@section('heading', 'Dashboard')

@section('content')
    <div class="grid gap-6 md:grid-cols-3">
        <article class="rounded-[2rem] border border-white/10 bg-white/5 p-6">
            <p class="text-sm uppercase tracking-[0.24em] text-slate-400">Blog Posts</p>
            <p class="mt-4 text-4xl font-semibold text-white">{{ $blogCount }}</p>
        </article>
        <article class="rounded-[2rem] border border-white/10 bg-white/5 p-6">
            <p class="text-sm uppercase tracking-[0.24em] text-slate-400">Published</p>
            <p class="mt-4 text-4xl font-semibold text-white">{{ $publishedCount }}</p>
        </article>
        <article class="rounded-[2rem] border border-white/10 bg-white/5 p-6">
            <p class="text-sm uppercase tracking-[0.24em] text-slate-400">Admins</p>
            <p class="mt-4 text-4xl font-semibold text-white">{{ $adminCount }}</p>
        </article>
    </div>

    <div class="mt-8 grid gap-8 xl:grid-cols-[1.1fr_0.9fr]">
        <section class="rounded-[2rem] border border-white/10 bg-white/5 p-6">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm uppercase tracking-[0.24em] text-slate-400">Publishing</p>
                    <h3 class="mt-2 text-2xl font-semibold text-white">Latest blog activity</h3>
                </div>
                <a href="{{ route('admin.blogs.create') }}" class="rounded-full bg-emerald-400 px-4 py-2 text-sm font-semibold text-slate-950">New Post</a>
            </div>
            <div class="mt-6 space-y-4">
                @foreach ($latestPosts as $post)
                    <div class="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
                        <div class="flex items-center justify-between gap-4">
                            <div>
                                <p class="text-base font-semibold text-white">{{ $post->title }}</p>
                                <p class="mt-1 text-sm text-slate-400">{{ $post->excerpt }}</p>
                            </div>
                            <span class="rounded-full px-3 py-1 text-xs font-semibold {{ $post->is_published ? 'bg-emerald-400/15 text-emerald-200' : 'bg-amber-400/15 text-amber-200' }}">
                                {{ $post->is_published ? 'Published' : 'Draft' }}
                            </span>
                        </div>
                    </div>
                @endforeach
            </div>
        </section>

        <section class="rounded-[2rem] border border-white/10 bg-white/5 p-6">
            <p class="text-sm uppercase tracking-[0.24em] text-slate-400">Admin Access</p>
            <h3 class="mt-2 text-2xl font-semibold text-white">Seeded login</h3>
            <div class="mt-6 rounded-2xl border border-white/10 bg-slate-950/60 p-5 text-sm text-slate-300">
                <p><span class="font-semibold text-white">Email:</span> janonemersion@hotmail.com</p>
                <p class="mt-2"><span class="font-semibold text-white">Password:</span> Jj112112@!@!</p>
                <p class="mt-4 text-slate-400">This account is seeded automatically so the admin workspace is usable immediately after setup.</p>
            </div>
        </section>
    </div>
@endsection
""",
        "resources/views/admin/blogs/index.blade.php": """@extends('layouts.admin')

@section('title', 'Manage Blogs')
@section('eyebrow', 'Publishing')
@section('heading', 'Manage Blogs')

@section('content')
    <div class="flex items-center justify-between gap-4">
        <p class="text-sm text-slate-400">Manage the dynamic blog feed, update posts, and keep the public site fresh.</p>
        <a href="{{ route('admin.blogs.create') }}" class="rounded-full bg-emerald-400 px-4 py-2 text-sm font-semibold text-slate-950">Create Post</a>
    </div>

    <div class="mt-8 overflow-hidden rounded-[2rem] border border-white/10">
        <table class="min-w-full divide-y divide-white/10">
            <thead class="bg-white/5">
                <tr>
                    <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Title</th>
                    <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Status</th>
                    <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Published</th>
                    <th class="px-6 py-4"></th>
                </tr>
            </thead>
            <tbody class="divide-y divide-white/10 bg-slate-950/50">
                @foreach ($blogPosts as $post)
                    <tr>
                        <td class="px-6 py-5">
                            <p class="font-semibold text-white">{{ $post->title }}</p>
                            <p class="mt-1 text-sm text-slate-400">{{ $post->slug }}</p>
                        </td>
                        <td class="px-6 py-5 text-sm text-slate-300">{{ $post->is_published ? 'Published' : 'Draft' }}</td>
                        <td class="px-6 py-5 text-sm text-slate-300">{{ optional($post->published_at)->format('M d, Y') ?: 'Not set' }}</td>
                        <td class="px-6 py-5">
                            <div class="flex items-center justify-end gap-3">
                                <a href="{{ route('admin.blogs.edit', $post) }}" class="text-sm font-semibold text-emerald-300">Edit</a>
                                <form method="POST" action="{{ route('admin.blogs.destroy', $post) }}">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit" class="text-sm font-semibold text-rose-300">Delete</button>
                                </form>
                            </div>
                        </td>
                    </tr>
                @endforeach
            </tbody>
        </table>
    </div>

    <div class="mt-8">
        {{ $blogPosts->links() }}
    </div>
@endsection
""",
        "resources/views/admin/blogs/form.blade.php": """@extends('layouts.admin')

@section('title', $mode === 'create' ? 'Create Blog Post' : 'Edit Blog Post')
@section('eyebrow', 'Publishing')
@section('heading', $mode === 'create' ? 'Create Blog Post' : 'Edit Blog Post')

@section('content')
    <form method="POST" action="{{ $mode === 'create' ? route('admin.blogs.store') : route('admin.blogs.update', $blogPost) }}" class="space-y-6 rounded-[2rem] border border-white/10 bg-white/5 p-6">
        @csrf
        @if ($mode === 'edit')
            @method('PUT')
        @endif

        <div class="grid gap-6 lg:grid-cols-2">
            <div class="lg:col-span-2">
                <label class="mb-2 block text-sm font-medium text-slate-200">Title</label>
                <input name="title" value="{{ old('title', $blogPost->title) }}" class="w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 text-white">
            </div>
            <div class="lg:col-span-2">
                <label class="mb-2 block text-sm font-medium text-slate-200">Slug</label>
                <input name="slug" value="{{ old('slug', $blogPost->slug) }}" class="w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 text-white">
            </div>
            <div class="lg:col-span-2">
                <label class="mb-2 block text-sm font-medium text-slate-200">Excerpt</label>
                <textarea name="excerpt" rows="3" class="w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 text-white">{{ old('excerpt', $blogPost->excerpt) }}</textarea>
            </div>
            <div class="lg:col-span-2">
                <label class="mb-2 block text-sm font-medium text-slate-200">Content</label>
                <textarea name="content" rows="12" class="w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 text-white">{{ old('content', $blogPost->content) }}</textarea>
            </div>
            <div>
                <label class="mb-2 block text-sm font-medium text-slate-200">Published At</label>
                <input type="datetime-local" name="published_at" value="{{ old('published_at', optional($blogPost->published_at)->format('Y-m-d\\TH:i')) }}" class="w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 text-white">
            </div>
            <div class="flex items-center gap-3 pt-8">
                <input id="is_published" type="checkbox" name="is_published" value="1" @checked(old('is_published', $blogPost->is_published)) class="h-5 w-5 rounded border-white/20 bg-slate-950/80 text-emerald-400">
                <label for="is_published" class="text-sm font-medium text-slate-200">Publish immediately</label>
            </div>
        </div>

        <div class="flex items-center gap-3">
            <button type="submit" class="rounded-full bg-emerald-400 px-5 py-3 text-sm font-semibold text-slate-950">Save Post</button>
            <a href="{{ route('admin.blogs.index') }}" class="rounded-full border border-white/10 px-5 py-3 text-sm font-semibold text-white">Cancel</a>
        </div>
    </form>
@endsection
""",
        "routes/web.php": """<?php

use App\\Http\\Controllers\\Admin\\BlogPostController as AdminBlogPostController;
use App\\Http\\Controllers\\Admin\\DashboardController;
use App\\Http\\Controllers\\BlogController;
use App\\Http\\Controllers\\PageController;
use App\\Http\\Controllers\\ProfileController;
use Illuminate\\Support\\Facades\\Route;

Route::get('/', [PageController::class, 'home'])->name('home');
Route::get('/about-us', [PageController::class, 'about'])->name('about');
Route::get('/media', [PageController::class, 'media'])->name('media');
Route::get('/blogs', [BlogController::class, 'index'])->name('blogs.index');
Route::get('/blogs/{blogPost:slug}', [BlogController::class, 'show'])->name('blogs.show');
Route::get('/contact-us', [PageController::class, 'contact'])->name('contact');
Route::post('/contact-us', [PageController::class, 'submitContact'])->name('contact.submit');

Route::get('/dashboard', function () {
    return redirect()->route('admin.dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

Route::middleware(['auth', 'admin'])->prefix('admin')->name('admin.')->group(function () {
    Route::get('/', DashboardController::class)->name('dashboard');
    Route::resource('blogs', AdminBlogPostController::class)->except(['show']);
});

require __DIR__.'/auth.php';
""",
        "tests/Feature/ExampleTest.php": """<?php

namespace Tests\\Feature;

use Illuminate\\Foundation\\Testing\\RefreshDatabase;
use Tests\\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
""",
        "app/Models/User.php": """<?php

namespace App\\Models;

// use Illuminate\\Contracts\\Auth\\MustVerifyEmail;
use Database\\Factories\\UserFactory;
use Illuminate\\Database\\Eloquent\\Attributes\\Fillable;
use Illuminate\\Database\\Eloquent\\Attributes\\Hidden;
use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
use Illuminate\\Foundation\\Auth\\User as Authenticatable;
use Illuminate\\Notifications\\Notifiable;

#[Fillable(['name', 'email', 'password', 'is_admin'])]
#[Hidden(['password', 'remember_token'])]
class User extends Authenticatable
{
    /** @use HasFactory<UserFactory> */
    use HasFactory, Notifiable;

    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
            'is_admin' => 'boolean',
        ];
    }
}
""",
    }
    return files
