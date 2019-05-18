<?php

namespace App\Http\Controllers;

use App\Recipe;
use View;
use Illuminate\Http\Request;
use Carbon;
class RecipeController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $r = Recipe::inRandomOrder()->first();
        $recent = $this->getRecentRecipes(10);
        $r->views = $r->views+1;
        $r->save();
        $total = Recipe::count();
        return View::make('home', array('r' => $r, 'total'=>$total, 'recent'=>$recent));
    }

   public function view(Recipe $r){
        $recent = $this->getRecentRecipes(10);
        $r->views = $r->views+1;
        $r->save = true;
        $r->save();
        $total = Recipe::count();
        return View::make('home', array('r' => $r, 'total'=>$total, 'recent'=>$recent));
   }


   private function getRecentRecipes($n){
        $recents = Recipe::latest()->take($n)->select('title','id','created_at')->get();
        foreach ($recents as $key => &$recent) {
            $date = $recent->created_at->format('d-m-Y H:i:s');
            $recent->timeAgo = Carbon\Carbon::parse($date, 'America/Denver')->diffForHumans();
        }
        return $recents;
   }
}
