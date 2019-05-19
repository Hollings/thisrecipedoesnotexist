<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;

class SendRecipeToTwitter extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'send:recipe';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Sends recipe to twitter';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $r = \App\Recipe::inRandomOrder()->first();
        $r->notify(new \App\Notifications\RecipeCreated());
    }
}
