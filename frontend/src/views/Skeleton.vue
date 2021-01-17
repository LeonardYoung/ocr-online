<!--
 * @Author: your name
 * @Date: 2021-01-16 21:41:49
 * @LastEditTime: 2021-01-17 15:17:11
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\views\Skeleton.Vue
-->
<template>
	<a-layout class="layer">
		<a-layout-header class="header">
			<a-button class="back" type="primary" @click="backHome">
				返回
			</a-button>
				<h1 class="title">{{title}}</h1>

		</a-layout-header>
		<a-layout>
			<a-layout-sider class="sider">
        
				<slot name="sider"></slot>
			</a-layout-sider>
			<a-layout-content>
        <a-row type="flex" justify="space-around">
          <a-col span="11">
            <slot name="contentLeft"></slot>
          </a-col>
          <a-col span="11">
            <slot name="contentRight"></slot>
          </a-col>
        </a-row>
				
			</a-layout-content>
		</a-layout>
		
		
<!-- 		<a-layout-footer class="footer">
			<slot name="footer"></slot>
		</a-layout-footer> -->
	</a-layout>
</template>

<script type="text/ecmascript-6">
	export default {
		props: {
			title: String
		},
		components: {},
		data() {
			return {};
		},
		methods: {
			backHome(){
				this.$router.push({ path: "/" });
			}
		},
	};
</script>

<style scoped>
	.header {
		background-color: skyblue;
		font-size: 3rem;
		height: 10%;
		display: flex;
		position: relative;
	}
	.back{
		position: absolute;
		top: 50%;
		transform: translate(0,-50%);
	}
	.title{
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%,-50%);
	}

	.layer {
		width: 100%;
		height: 100%;
	}

	.sider {
		background-color: white;
		/* width: 15%; */
	}
</style>
