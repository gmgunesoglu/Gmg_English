import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './admin.component';
import {HomeComponent} from "../admin/home/home.component";
import {ReadingComponent} from "../admin/reading/reading.component";

const routes: Routes = [
  { path: '', component: AdminComponent, children: [
      { path: '', component: HomeComponent }, // Ana sayfa
      { path: 'reading', component: ReadingComponent },
    ] }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
