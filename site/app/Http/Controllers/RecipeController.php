<?php

namespace App\Http\Controllers;

use App\Recipe;
use View;
use Illuminate\Http\Request;

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
        $r->views = $r->views+1;
        $r->save();
        $total = Recipe::count();
        return View::make('home', array('r' => $r, 'total'=>$total));
    }

   public function view(Recipe $r){
        $r->views = $r->views+1;
        $r->save = true;
        $r->save();
        $total = Recipe::count();
        return View::make('home', array('r' => $r, 'total'=>$total));
   }
}
