import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BaseComponent } from './base.component';
import {ReadingComponent} from "./reading/reading.component";
import {HomeComponent} from "./home/home.component";
import { WebScoketComponent } from './web-scoket/web-scoket.component';

// const routes: Routes = [
//   { path: '', component: BaseComponent },
//   { path: 'reading', component: ReadingComponent },
//   { path: 'home', component: HomeComponent },
// ];

const routes: Routes = [
  {
    path: '',
    component: BaseComponent,
    children: [
      { path: '', component: HomeComponent }, // Ana sayfa
      { path: 'reading', component: ReadingComponent },
      { path: 'home', component: HomeComponent },
      { path: 'ws', component: WebScoketComponent},
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BaseRoutingModule { }
